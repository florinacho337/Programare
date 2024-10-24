import { useCallback, useEffect, useReducer } from 'react';
import { getLogger } from '../core';
import { TaskProps } from './TaskProps';
import { getTasks } from './taskApi';

const log = getLogger('useTasks');

export interface TasksState {
  tasks?: TaskProps[],
  fetching: boolean,
  fetchingError?: Error,
}

export interface TasksProps extends TasksState {
  addTask: () => void,
}

interface ActionProps {
  type: string,
  payload?: any,
}

const initialState: TasksState = {
  tasks: undefined,
  fetching: false,
  fetchingError: undefined,
};

const FETCH_TASKS_STARTED = 'FETCH_TASKS_STARTED';
const FETCH_TASKS_SUCCEEDED = 'FETCH_TASKS_SUCCEEDED';
const FETCH_TASKS_FAILED = 'FETCH_TASKS_FAILED';

const reducer: (state: TasksState, action: ActionProps) => TasksState =
  (state, { type, payload }) => {
    switch(type) {
      case FETCH_TASKS_STARTED:
        return { ...state, fetching: true };
      case FETCH_TASKS_SUCCEEDED:
        return { ...state, tasks: payload.tasks, fetching: false };
      case FETCH_TASKS_FAILED:
        return { ...state, fetchingError: payload.error, fetching: false };
      default:
        return state;
    }
  };

export const useTasks: () => TasksProps = () => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const { tasks, fetching, fetchingError } = state;
  const addTask = useCallback(() => {
    log('addTask - TODO');
  }, []);
  useEffect(getTasksEffect, [dispatch]);
  log(`returns - fetching = ${fetching}, tasks = ${JSON.stringify(tasks)}`);
  return {
    tasks,
    fetching,
    fetchingError,
    addTask,
  };

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
};
