import axios from 'axios';
import { getLogger, withLogs, authConfig, baseUrl } from '../core';
import { TaskProps } from './TaskProps';

const taskUrl = `http://${baseUrl}/api/task`;

export const getTasks: (token: string) => Promise<TaskProps[]> = token => {
  return withLogs(axios.get(taskUrl, authConfig(token)), 'getTasks');
}

export const createTask: (token: string, task: TaskProps) => Promise<TaskProps[]> = (token, task) => {
  return withLogs(axios.post(taskUrl, task, authConfig(token)), 'createTask');
}

export const updateTask: (token: string, task: TaskProps) => Promise<TaskProps[]> = (token, task) => {
  return withLogs(axios.put(`${taskUrl}/${task._id}`, task, authConfig(token)), 'updateTask');
}

interface MessageData {
  type: string;
  payload: TaskProps;
}

const log = getLogger('ws');

export const newWebSocket = (token: string, onMessage: (data: MessageData) => void, onOpen: () => void, onClose: () => void) => {
  const ws = new WebSocket(`ws://${baseUrl}`);
  ws.onopen = () => {
    log('web socket onopen');
    ws.send(JSON.stringify({ type: 'authorization', payload: { token } }));
    onOpen();
  };
  ws.onclose = () => {
    log('web socket onclose');
    onClose();
  };
  ws.onerror = error => {
    log('web socket onerror', error);
  };
  ws.onmessage = messageEvent => {
    log('web socket onmessage');
    onMessage(JSON.parse(messageEvent.data));
  };
  return () => {
    ws.close();
  };
}