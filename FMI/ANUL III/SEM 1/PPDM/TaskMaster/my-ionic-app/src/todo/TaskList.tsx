import React, { useContext, useState } from 'react';
import { RouteComponentProps } from 'react-router';
import {
  IonContent,
  IonHeader,
  IonIcon,
  IonLoading,
  IonPage,
  IonTitle,
  IonToolbar,
  IonGrid,
  IonRow,
  IonCol,
  IonButton
} from '@ionic/react';
import { add, sunny, moon } from 'ionicons/icons';
import Task from './Task';
import { getLogger } from '../core';
import { TaskContext } from './TaskProvider';
import './TaskList.css'; // Import the CSS file

const log = getLogger('TaskList');

const TaskList: React.FC<RouteComponentProps> = ({ history }) => {
  const { tasks, fetching, fetchingError, saveTask } = useContext(TaskContext);
  const [darkMode, setDarkMode] = useState(false);

  const toggleDarkModeHandler = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle('dark', !darkMode);
    document.body.classList.toggle('light', darkMode);
  };

  const handleAddTask = () => {
    history.push('/task');
  };

  const handleToggleFinished = (id?: string) => {
    const task = tasks?.find(t => t.id === id);
    if (task) {
      const updatedTask = { ...task, finished: !task.finished };
      saveTask && saveTask(updatedTask);
    }
  };

  log('render');
  return (
    <IonPage className={darkMode ? 'dark' : 'light'}>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Task Master</IonTitle>
          <IonButton slot="end" fill="clear" onClick={toggleDarkModeHandler}>
            <IonIcon icon={darkMode ? sunny : moon} style={{ color: darkMode ? 'inherit' : '#000' }} />
          </IonButton>
        </IonToolbar>
      </IonHeader>
      <IonContent className="ion-padding">
        <IonLoading isOpen={fetching} message="Fetching tasks" />
        <IonGrid>
          <IonRow>
            <IonCol size="12" size-md="6">
              <div className="post-it add-task" onClick={handleAddTask}>
                <div className="pin"></div>
                <IonIcon icon={add} className="add-icon" />
                <div className="add-text">Add new task</div>
              </div>
            </IonCol>
            {tasks && tasks.map(task => (
              <IonCol size="12" size-md="6" key={task.id}>
                <Task {...task} onEdit={id => history.push(`/task/${id}`)} onToggleFinished={handleToggleFinished} />
              </IonCol>
            ))}
          </IonRow>
        </IonGrid>
        {fetchingError && (
          <div>{fetchingError.message || 'Failed to fetch tasks'}</div>
        )}
      </IonContent>
    </IonPage>
  );
};

export default TaskList;