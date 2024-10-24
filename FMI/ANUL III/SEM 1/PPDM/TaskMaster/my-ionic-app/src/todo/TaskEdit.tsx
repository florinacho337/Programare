import React, { useCallback, useContext, useEffect, useState } from 'react';
import {
  IonButton,
  IonButtons,
  IonContent,
  IonHeader,
  IonInput,
  IonLoading,
  IonPage,
  IonTitle,
  IonToolbar,
  IonItem,
  IonLabel,
  IonDatetime,
  IonTextarea,
  IonRange,
  IonToggle,
  IonText,
  IonIcon,
  IonAlert
} from '@ionic/react';
import { save } from 'ionicons/icons'; // Import the save icon
import { getLogger } from '../core';
import { TaskContext } from './TaskProvider';
import { RouteComponentProps } from 'react-router';
import { TaskProps } from './TaskProps';
import './TaskEdit.css'; // Import the CSS file

const log = getLogger('TaskEdit');

interface TaskEditProps extends RouteComponentProps<{
  id?: string;
}> {}

const TaskEdit: React.FC<TaskEditProps> = ({ history, match }) => {
  const { tasks, saving, savingError, saveTask } = useContext(TaskContext);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [deadline, setDeadline] = useState<Date>(new Date());
  const [progress, setProgress] = useState(0);
  const [important, setImportant] = useState(false);
  const [urgent, setUrgent] = useState(false);
  const [finished, setFinished] = useState(false);
  const [task, setTask] = useState<TaskProps>();
  const [showDatetimePicker, setShowDatetimePicker] = useState(false);
  const [showAlert, setShowAlert] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');
  const [pinColor, setPinColor] = useState('medium');

  useEffect(() => {
    log('useEffect');
    const routeId = match.params.id || '';
    const task = tasks?.find(t => t.id === routeId);
    setTask(task);
    if (task) {
      setName(task.name);
      setDescription(task.description || '');
      setDeadline(new Date(task.deadline));
      setProgress(task.progress);
      setImportant(task.important);
      setUrgent(task.urgent);
      setFinished(task.finished || false);
    }
  }, [match.params.id, tasks]);

  useEffect(() => {
    setPinColor(important && urgent ? 'danger' : important ? 'success' : urgent ? 'secondary' : 'medium');
  }, [important, urgent]);

  const validateTask = (task: TaskProps) => {
    if (!task.name || !task.deadline || task.important === undefined || task.urgent === undefined || task.progress < 0
      || task.progress > 100 || task.finished === undefined) {
      setAlertMessage('The task has invalid information!');
      setShowAlert(true);
      return false;
    }
    return true;
  };

  const handleSave = useCallback(() => {
    const editedTask = task ? { ...task, name, description, deadline, progress, important, urgent, finished } : { name, description, deadline, progress, important, urgent, finished };
    if (validateTask(editedTask)) {
      saveTask && saveTask(editedTask).then(() => history.goBack());
    }
  }, [task, saveTask, name, description, deadline, progress, important, urgent, finished, history]);

  log('render');
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>{task ? "Edit Task": "Save Task"}</IonTitle>
          <IonButtons slot="end">
            <IonButton onClick={handleSave}>
              <IonIcon icon={save} />
            </IonButton>
          </IonButtons>
        </IonToolbar>
      </IonHeader>
      <IonContent className="ion-padding">
        <div className="post-it">
          <div className={`pin ${pinColor}`}></div>
          <IonItem className="post-it-item">
            <IonLabel position="stacked">Name</IonLabel>
            <IonInput value={name} onIonChange={e => setName(e.detail.value || '')} />
          </IonItem>
          <IonItem className="post-it-item" button onClick={() => setShowDatetimePicker(!showDatetimePicker)}>
            <IonLabel position="stacked">Deadline</IonLabel>
            <IonText>{deadline ? deadline.toLocaleDateString() : 'Select a date'}</IonText>
          </IonItem>
          { showDatetimePicker && <IonDatetime
            presentation="date"
            value={deadline ? deadline.toISOString() : ''}
            onIonChange={e => {
              setDeadline(new Date(e.detail.value as string));
              setShowDatetimePicker(false);
            }}
            onIonCancel={() => setShowDatetimePicker(false)}
          /> }
          <IonItem className="post-it-item">
            <IonLabel position="stacked">Description</IonLabel>
            <IonTextarea placeholder="Add a description..." value={description} onIonChange={e => setDescription(e.detail.value || '')} />
          </IonItem>
          <IonItem className="post-it-item">
            <IonLabel position="stacked">Progress</IonLabel>
            <IonRange min={0} max={100} value={progress} onIonChange={e => setProgress(e.detail.value as number)}>
              <IonLabel slot="end">{progress}%</IonLabel>
            </IonRange>
          </IonItem>
          <IonItem className="post-it-item">
            <IonLabel>Important</IonLabel>
            <IonToggle checked={important} onIonChange={e => setImportant(e.detail.checked)} />
          </IonItem>
          <IonItem className="post-it-item">
            <IonLabel>Urgent</IonLabel>
            <IonToggle checked={urgent} onIonChange={e => setUrgent(e.detail.checked)} />
          </IonItem>
        </div>
        <IonLoading isOpen={saving} />
        {savingError && (
          <div>{savingError.message || 'Failed to save task'}</div>
        )}
        <IonAlert
          isOpen={showAlert}
          onDidDismiss={() => setShowAlert(false)}
          header={'Error'}
          message={alertMessage}
          buttons={['OK']}
        />
      </IonContent>
    </IonPage>
  );
};

export default TaskEdit;