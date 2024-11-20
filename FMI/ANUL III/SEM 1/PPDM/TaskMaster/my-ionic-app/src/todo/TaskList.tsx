import React, { useContext, useState, useEffect, useMemo } from 'react';
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
  IonButton,
  IonSelect,
  IonSelectOption,
  IonItem,
  IonSearchbar,
  IonInfiniteScroll,
  IonInfiniteScrollContent,
  IonFab,
  IonFabButton,
  IonModal
} from '@ionic/react';
import { add, sunny, moon, logOut, map } from 'ionicons/icons'; // Import the map icon
import Task from './Task';
import { getLogger } from '../core';
import { TaskContext } from './TaskProvider';
import './TaskList.css'; // Import the CSS file
import { AuthContext } from '../auth/AuthProvider';
import { TaskProps } from './TaskProps';
import MyMap from '../components/MyMap'; // Import the MyMap component

const log = getLogger('TaskList');

const TaskList: React.FC<RouteComponentProps> = ({ history }) => {
  const { tasks, fetching, fetchingError, saveTask } = useContext(TaskContext);
  const { logout } = useContext(AuthContext);
  const [darkMode, setDarkMode] = useState(false);
  const [searchText, setSearchText] = useState('');
  const [filter, setFilter] = useState('all');
  const [displayedTasks, setDisplayedTasks] = useState<TaskProps[]>([]);
  const [page, setPage] = useState(1);
  const [showMapModal, setShowMapModal] = useState(false);

  const toggleDarkModeHandler = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle('dark', !darkMode);
    document.body.classList.toggle('light', darkMode);
  };

  const handleAddTask = () => {
    history.push('/task');
  };

  const handleToggleFinished = (_id?: string) => {
    const task = tasks?.find(t => t._id === _id);
    if (task) {
      const updatedTask = { ...task, finished: !task.finished };
      saveTask && saveTask(updatedTask);
    }
  };

  const filteredTasks = useMemo(() => {
    return tasks?.filter(task => {
      const matchesSearch = task.name.toLowerCase().includes(searchText.toLowerCase());
      const matchesFilter = filter === 'all' || (filter === 'finished' && task.finished) || (filter === 'unfinished' && !task.finished);
      return matchesSearch && matchesFilter;
    });
  }, [tasks, searchText, filter]);

  useEffect(() => {
    setDisplayedTasks(filteredTasks?.slice(0, page * 3) || []);
  }, [filteredTasks, page]);

  const loadMoreTasks = () => {
    setPage(prevPage => prevPage + 1);
  };

  const handleShowMap = () => {
    setShowMapModal(true);
  };

  log('render', fetching);
  return (
    <IonPage className={darkMode ? 'dark' : 'light'}>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Task Master</IonTitle>
          <IonButton slot="end" fill="clear" onClick={toggleDarkModeHandler}>
            <IonIcon icon={darkMode ? sunny : moon} style={{ color: darkMode ? 'inherit' : '#000' }} />
          </IonButton>
          <IonButton slot="end" fill="clear" onClick={logout}>
            <IonIcon icon={logOut} style={{ color: darkMode ? 'inherit' : '#000' }} />
          </IonButton>
        </IonToolbar>
      </IonHeader>
      <IonContent className="ion-padding">
        <IonItem>
          <IonSearchbar
            value={searchText}
            placeholder="Search tasks"
            onIonChange={e => setSearchText(e.detail.value!)}
          />
          <IonSelect
            value={filter}
            placeholder="Filter"
            onIonChange={e => setFilter(e.detail.value)}
          >
            <IonSelectOption value="all">All</IonSelectOption>
            <IonSelectOption value="finished">Finished</IonSelectOption>
            <IonSelectOption value="unfinished">Unfinished</IonSelectOption>
          </IonSelect>
        </IonItem>
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
            {displayedTasks && displayedTasks.map(task => (
              <IonCol size="12" size-md="6" key={task._id}>
                <Task {...task} onEdit={id => history.push(`/task/${id}`)} onToggleFinished={handleToggleFinished} />
              </IonCol>
            ))}
          </IonRow>
        </IonGrid>
        {fetchingError && (
          <div>{fetchingError.message || 'Failed to fetch tasks'}</div>
        )}
        <IonInfiniteScroll
          onIonInfinite={(e: CustomEvent<void>) => {
            loadMoreTasks();
            (e.target as HTMLIonInfiniteScrollElement).complete();
          }}
          threshold="100px"
          disabled={displayedTasks.length >= (filteredTasks?.length || 0)}
        >
          <IonInfiniteScrollContent loadingText="Loading more tasks..."></IonInfiniteScrollContent>
        </IonInfiniteScroll>
        <IonFab vertical="bottom" horizontal="end" slot="fixed">
          <IonFabButton onClick={handleShowMap}>
            <IonIcon icon={map} />
          </IonFabButton>
        </IonFab>
        <IonModal isOpen={showMapModal} onDidDismiss={() => setShowMapModal(false)}>
          <MyMap tasks={tasks || []} enterTask={id => history.push(`/task/${id}`)} showExistingMarkers={true} />
          <IonButton onClick={() => setShowMapModal(false)}>Close Map</IonButton>
        </IonModal>
      </IonContent>
    </IonPage>
  );
};

export default TaskList;