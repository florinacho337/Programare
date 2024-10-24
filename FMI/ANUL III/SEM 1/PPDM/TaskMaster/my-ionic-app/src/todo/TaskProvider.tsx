import React, { useCallback, useEffect, useReducer } from 'react';
import PropTypes from 'prop-types';
import { getLogger } from '../core';
import { TaskProps } from './TaskProps';
import { createTask, getTasks, newWebSocket, updateTask } from './taskApi';

const log = getLogger('TaskProvider');

type SaveTaskFn = (task: TaskProps) => Promise<any>;

export interface TasksState {
  tasks?: TaskProps[],
  fetching: boolean,
  fetchingError?: Error | null,
  saving: boolean,
  savingError?: Error | null,
  saveTask?: SaveTaskFn,
}

interface ActionProps {
  type: string,
  payload?: any,
}

const initialState: TasksState = {
  fetching: false,
  saving: false,
};

const FETCH_TASKS_STARTED = 'FETCH_TASKS_STARTED';
const FETCH_TASKS_SUCCEEDED = 'FETCH_TASKS_SUCCEEDED';
const FETCH_TASKS_FAILED = 'FETCH_TASKS_FAILED';
const SAVE_TASK_STARTED = 'SAVE_TASK_STARTED';
const SAVE_TASK_SUCCEEDED = 'SAVE_TASK_SUCCEEDED';
const SAVE_TASK_FAILED = 'SAVETASK_FAILED';

const reducer: (state: TasksState, action: ActionProps) => TasksState =
  (state, { type, payload }) => {
    switch(type) {
      case FETCH_TASKS_STARTED:
        return { ...state, fetching: true, fetchingError: null };
      case FETCH_TASKS_SUCCEEDED:
        return { ...state, tasks: payload.tasks, fetching: false };
      case FETCH_TASKS_FAILED:
        return { ...state, fetchingError: payload.error, fetching: false };
      case SAVE_TASK_STARTED:
        return { ...state, savingError: null, saving: true };
      case SAVE_TASK_SUCCEEDED:
        const tasks = [...(state.tasks || [])];
        const task = payload.task;
        const index = tasks.findIndex(it => it.id === task.id);
        if (index === -1) {
          tasks.splice(0, 0, task);
        } else {
          tasks[index] = task;
        }
        return { ...state,  tasks: tasks, saving: false };
      case SAVE_TASK_FAILED:
        return { ...state, savingError: payload.error, saving: false };
      default:
        return state;
    }
  };

export const TaskContext = React.createContext<TasksState>(initialState);

interface TaskProviderProps {
  children: PropTypes.ReactNodeLike,
}

export const TaskProvider: React.FC<TaskProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const { tasks, fetching, fetchingError, saving, savingError } = state;
  useEffect(getTasksEffect, []);
  useEffect(wsEffect, []);
  const saveTask = useCallback<SaveTaskFn>(saveTaskCallback, []);
  const value = { tasks, fetching, fetchingError, saving, savingError, saveTask };
  log('returns');
  return (
    <TaskContext.Provider value={value}>
      {children}
    </TaskContext.Provider>
  );

  function getTasksEffect() {
    let canceled = false;
    fetchTasks();
    return () => {
      canceled = true;
    }

    async function fetchTasks() {
      try {
        log('fetchTasks started');
        dispatch({ type: FETCH_TASKS_STARTED });
        const tasks = await getTasks();
        log('fetchTasks succeeded');
        if (!canceled) {
          dispatch({ type: FETCH_TASKS_SUCCEEDED, payload: { tasks } });
        }
      } catch (error) {
        log('fetchTasks failed');
        if (!canceled) {
          dispatch({ type: FETCH_TASKS_FAILED, payload: { error } });
        }
      }
    }
  }

  async function saveTaskCallback(task: TaskProps) {
    try {
      log('saveTask started');
      dispatch({ type: SAVE_TASK_STARTED });
      const savedTask = await (task.id ? updateTask(task) : createTask(task));
      log('saveTask succeeded');
      dispatch({ type: SAVE_TASK_SUCCEEDED, payload: { task: savedTask } });
    } catch (error) {
      log('saveTask failed');
      dispatch({ type: SAVE_TASK_FAILED, payload: { error } });
    }
  }

  function wsEffect() {
    let canceled = false;
    log('wsEffect - connecting');
    const closeWebSocket = newWebSocket(message => {
      if (canceled) {
        return;
      }
      const { event, payload: { task }} = message;
      log(`ws message, task ${event}`);
      if (event === 'created' || event === 'updated') {
        dispatch({ type: SAVE_TASK_SUCCEEDED, payload: { task } });
      }
    });
    return () => {
      log('wsEffect - disconnecting');
      canceled = true;
      closeWebSocket();
    }
  }
};
