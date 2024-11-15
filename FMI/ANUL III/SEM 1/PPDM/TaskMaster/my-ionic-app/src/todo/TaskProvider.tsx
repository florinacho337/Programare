import React, { useCallback, useEffect, useReducer, useContext, useState } from 'react';
import PropTypes from 'prop-types';
import { getLogger } from '../core';
import { TaskProps } from './TaskProps';
import { createTask, getTasks, newWebSocket, updateTask } from './taskApi';
import { AuthContext } from '../auth';
import { Preferences } from '@capacitor/preferences';
import { Network } from '@capacitor/network';
import { v4 as uuidv4 } from 'uuid'; 

const log = getLogger('TaskProvider');

type SaveTaskFn = (task: TaskProps) => Promise<any>;

export interface TasksState {
  tasks?: TaskProps[],
  fetching: boolean,
  fetchingError?: Error | null,
  saving: boolean,
  savingError?: Error | null,
  saveTask?: SaveTaskFn,
  offlineTasks?: TaskProps[],
}

interface ActionProps {
  type: string,
  payload?: any,
}

const initialState: TasksState = {
  fetching: false,
  saving: false,
  offlineTasks: [],
};

const FETCH_TASKS_STARTED = 'FETCH_TASKS_STARTED';
const FETCH_TASKS_SUCCEEDED = 'FETCH_TASKS_SUCCEEDED';
const FETCH_TASKS_FAILED = 'FETCH_TASKS_FAILED';
const SAVE_TASK_STARTED = 'SAVE_TASK_STARTED';
const SAVE_TASK_SUCCEEDED = 'SAVE_TASK_SUCCEEDED';
const ADD_OFFLINE_TASK = 'ADD_OFFLINE_TASK';
const REMOVE_OFFLINE_TASK = 'REMOVE_OFFLINE_TASK';

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
        const index = tasks.findIndex(t => t._id === task._id);
        if (index === -1) {
          tasks.splice(0, 0, task);
        } else {
          tasks[index] = task;
        }
        return { ...state,  tasks, saving: false };
      case ADD_OFFLINE_TASK:
        return { ...state, offlineTasks: [...(state.offlineTasks || []), payload.task] };
      case REMOVE_OFFLINE_TASK:
        return { ...state, offlineTasks: (state.offlineTasks || []).filter(t => t._id !== payload.task._id) };
      default:
        return state;
    }
  };

export const TaskContext = React.createContext<TasksState>(initialState);

interface TaskProviderProps {
  children: PropTypes.ReactNodeLike,
}

export const TaskProvider: React.FC<TaskProviderProps> = ({ children }) => {
  const { token } = useContext(AuthContext);
  const [state, dispatch] = useReducer(reducer, initialState);
  const { tasks, fetching, fetchingError, saving, savingError, offlineTasks } = state;
  const [networkStatus, setNetworkStatus] = useState<boolean>(true);

  useEffect(getTasksEffect, [token]);
  useEffect(wsEffect, [token]);
  useEffect(() => {
    const handler = Network.addListener('networkStatusChange', async (status) => {
      log('network status changed', status);
      setNetworkStatus(status.connected);
      if (status.connected) {
        await syncOfflineTasks(token);
        getTasksEffect();
      }
    });

    return () => {
      handler.then(h => h.remove());
    };
  }, [token]);

  const saveTask = useCallback<SaveTaskFn>(saveTaskCallback, [token, networkStatus]);
  const value = { tasks, fetching, fetchingError, saving, savingError, saveTask, offlineTasks };
  log('returns');
  return (
    <TaskContext.Provider value={value}>
      {children}
    </TaskContext.Provider>
  );

  function getTasksEffect() {
    let canceled = false;
    if (token) {
      fetchTasks();
    }
    return () => {
      canceled = true;
    }

    async function fetchTasks() {
      try {
        log('fetchTasks started');
        dispatch({ type: FETCH_TASKS_STARTED });
        const tasks = await getTasks(token);
        log('fetchTasks succeeded');
        if (!canceled) {
          dispatch({ type: FETCH_TASKS_SUCCEEDED, payload: { tasks } });
        }
      } catch (error) {
        log('fetchTasks failed');
        dispatch({ type: FETCH_TASKS_FAILED, payload: { error } });
      }
    }
  }

  async function syncOfflineTasks(token: string) {
    const offlineTasks = await Preferences.keys();
    for (const key of offlineTasks.keys) {
      if (key.startsWith('offlineTask-')) {
        const { value } = await Preferences.get({ key });
        if (value) {
          const task = JSON.parse(value);
          try {
            console.log('syncOfflineTasks started');
            // Check if the task has a temporary ID
            const isTemporaryId = task._id && task._id.startsWith('temp-');
            const savedTask = isTemporaryId 
              ? await createTask(token, task) // Create new task if it has a temporary ID
              : await updateTask(token, task); // Update existing task otherwise
            log('syncOfflineTasks succeeded');
            await Preferences.remove({ key });
            dispatch({ type: REMOVE_OFFLINE_TASK, payload: { task } });
            dispatch({ type: SAVE_TASK_SUCCEEDED, payload: { task: savedTask } });
          } catch (error) {
            log('syncOfflineTasks failed', error);
          }
        }
      }
    }
  }
  
  async function saveTaskCallback(task: TaskProps) {
    let savedOffline = false;
    try {
      log('saveTask started');
      dispatch({ type: SAVE_TASK_STARTED });
      if (networkStatus) {
        const savedTask = await (task._id ? updateTask(token, task) : createTask(token, task));
        log('saveTask succeeded');
        dispatch({ type: SAVE_TASK_SUCCEEDED, payload: { task: savedTask } });
      } else {
        log('saveTask offline');
        savedOffline = true;
        if (!task._id) {
          task._id = `temp-${uuidv4()}`; // Assign a temporary ID with a prefix if the task doesn't have one
        }
        dispatch({ type: ADD_OFFLINE_TASK, payload: { task } });
        await Preferences.set({ key: `offlineTask-${task._id}`, value: JSON.stringify(task) });
        dispatch({ type: SAVE_TASK_SUCCEEDED, payload: { task } }); // Update saving state to false
      }
    } catch (error) {
      log('saveTask failed');
      savedOffline = true;
      if (!task._id) {
        task._id = `temp-${uuidv4()}`; // Assign a temporary ID with a prefix if the task doesn't have one
      }
      dispatch({ type: ADD_OFFLINE_TASK, payload: { task } });
      await Preferences.set({ key: `offlineTask-${task._id}`, value: JSON.stringify(task) });
      dispatch({ type: SAVE_TASK_SUCCEEDED, payload: { task } }); // Update saving state to false
    }
    return savedOffline;
  }

  function wsEffect() {
    let canceled = false;
    log('wsEffect - connecting');
    let closeWebSocket: () => void;

    const connectWebSocket = () => {
      if (token?.trim()) {
        closeWebSocket = newWebSocket(token, message => {
          if (canceled) {
            return;
          }
          const { type, payload: task } = message;
          log(`, task ${type}`);
          if (type === 'created' || type === 'updated') {
            dispatch({ type: SAVE_TASK_SUCCEEDED, payload: { task } });
          }
        }, handleWebSocketOpen, handleWebSocketClose);
      }
    };

    const handleWebSocketOpen = async () => {
      log('WebSocket connected');
      await syncOfflineTasks(token);
      getTasksEffect();
    };

    const handleWebSocketClose = () => {
      if (!canceled) {
        log(`WebSocket closed, retrying in 5 seconds`);
        setTimeout(connectWebSocket, 5000);
      }
    };

    connectWebSocket();

    return () => {
      log('wsEffect - disconnecting');
      canceled = true;
      closeWebSocket?.();
    };
  }
};