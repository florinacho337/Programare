const Koa = require('koa');
const app = new Koa();
const server = require('http').createServer(app.callback());
const WebSocket = require('ws');
const wss = new WebSocket.Server({ server });
const Router = require('koa-router');
const cors = require('koa-cors');
const bodyparser = require('koa-bodyparser');

app.use(bodyparser());
app.use(cors());
app.use(async (ctx, next) => {
  const start = new Date();
  await next();
  const ms = new Date() - start;
  console.log(`${ctx.method} ${ctx.url} ${ctx.response.status} - ${ms}ms`);
});

app.use(async (ctx, next) => {
  await new Promise(resolve => setTimeout(resolve, 2000));
  await next();
});

app.use(async (ctx, next) => {
  try {
    await next();
  } catch (err) {
    ctx.response.body = { message: err.message || 'Unexpected error' };
    ctx.response.status = 500;
  }
});

class Task {
  constructor({ id, name, description, deadline, finished, progress, important, urgent }) {
    this.id = id;
    this.name = name;
    this.description = description;
    this.deadline = deadline;
    this.finished = finished;
    this.progress = progress;
    this.important = important;
    this.urgent = urgent;
  }
}

const tasks = [];
for (let i = 0; i < 3; i++) {
  tasks.push(new Task({ id: `${i}`, name: `task ${i}`, deadline: new Date(Date.now() + i), finshed: false, 
  progress: Math.floor(Math.random() * 100) + 1, important: true, urgent: false }));
}
let lastId = tasks[tasks.length - 1].id;

const broadcast = data =>
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(data));
    }
  });

const router = new Router();

router.get('/task', ctx => {
  ctx.response.body = tasks;
  ctx.response.status = 200;
});

router.get('/task/:id', async (ctx) => {
  const taskId = ctx.params.id;
  const task = tasks.find(task => taskId === task.id);
  if (task) {
    ctx.response.body = task;
    ctx.response.status = 200; // ok
  } else {
    ctx.response.body = { message: `task with id ${taskId} not found` };
    ctx.response.status = 404; // NOT FOUND (if you know the resource was deleted, then return 410 GONE)
  }
});

const createTask = async (ctx) => {
  const task = ctx.request.body;
  if (!task.name || !task.deadline || task.important === undefined || task.urgent === undefined || 
    (task.progress && (task.progress < 0 || task.progress > 100))) { // validation
    ctx.response.body = { message: 'The task has invalid information!' };
    ctx.response.status = 400; //  BAD REQUEST
    return;
  }
  task.id = `${parseInt(lastId) + 1}`;
  lastId = task.id;
  task.finished = false;
  if (!task.progress) {
    task.progress = 0;
  }
  tasks.push(task);
  ctx.response.body = task;
  ctx.response.status = 201; // CREATED
  broadcast({ event: 'created', payload: { task: task } });
};

router.post('/task', async (ctx) => {
  await createTask(ctx);
});

router.put('/task/:id', async (ctx) => {
  const id = ctx.params.id;
  const task = ctx.request.body;
  const taskId = task.id;
  if (taskId && id !== taskId) {
    ctx.response.body = { message: `Param id and body id should be the same` };
    ctx.response.status = 400; // BAD REQUEST
    return;
  }
  if (!taskId) {
    await createTask(ctx);
    return;
  }
  const index = tasks.findIndex(item => item.id === id);
  if (index === -1) {
    ctx.response.body = { message: `task with id ${id} not found` };
    ctx.response.status = 400; // BAD REQUEST
    return;
  }
  if (!task.name || !task.deadline || task.important === undefined || task.urgent === undefined || task.progress < 0
    || task.progress > 100 || task.finished === undefined) { // validation
    ctx.response.body = { message: 'The task has invalid information!' };
    ctx.response.status = 400; //  BAD REQUEST
    return;
  }
  tasks[index] = task;
  ctx.response.body = task;
  ctx.response.status = 200; // OK
  broadcast({ event: 'updated', payload: { task: task } });
});

router.del('/task/:id', ctx => {
  const id = ctx.params.id;
  const index = tasks.findIndex(task => id === task.id);
  if (index !== -1) {
    const task = tasks[index];
    tasks.splice(index, 1);
    broadcast({ event: 'deleted', payload: { task: task } });
  }
  ctx.response.status = 204; // no content
});

app.use(router.routes());
app.use(router.allowedMethods());

server.listen(3000);
