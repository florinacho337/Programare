import React, { useCallback, useContext, useEffect, useState, useRef } from 'react';
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
  IonAlert,
  IonToast,
  CreateAnimation
} from '@ionic/react';
import { save, informationOutline, camera } from 'ionicons/icons'; // Import the save and camera icons
import { getLogger } from '../core';
import { TaskContext } from './TaskProvider';
import { RouteComponentProps } from 'react-router';
import { TaskProps } from './TaskProps';
import './TaskEdit.css'; // Import the CSS file
import { usePhotoGallery, UserPhoto } from '../hooks/usePhotoGallery';

const log = getLogger('TaskEdit');

interface TaskEditProps extends RouteComponentProps<{
  _id?: string;
}> {}

const TaskEdit: React.FC<TaskEditProps> = ({ history, match }) => {
  const { tasks, saving, savingError, saveTask } = useContext(TaskContext);
  const { takePhoto, loadPhoto } = usePhotoGallery();
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
  const [showToast, setShowToast] = useState(false);
  const [photoFilePath, setPhotoFilePath] = useState<string>('');
  const [photo, setPhoto] = useState<string>();
  const animationRef = useRef<CreateAnimation>(null);

  useEffect(() => {
    log('useEffect');
    const routeId = match.params._id || '';
    const task = tasks?.find(t => t._id === routeId);
    setTask(task);
    if (task) {
      setName(task.name);
      setDescription(task.description || '');
      setDeadline(new Date(task.deadline));
      setProgress(task.progress);
      setImportant(task.important);
      setUrgent(task.urgent);
      setFinished(task.finished || false);
      setPhotoFilePath(task.photoFilePath || '');
    }
  }, [match.params._id, tasks]);

  useEffect(() => {
    if (photoFilePath) {
      loadPhoto(photoFilePath).then((photo) => setPhoto(photo.webviewPath));
    }
  }, [photoFilePath]);

  useEffect(() => {
    setPinColor(important && urgent ? 'danger' : important ? 'success' : urgent ? 'secondary' : 'medium');
  }, [important, urgent]);

  useEffect(() => {
    animationRef.current?.animation.play();
  }, []);

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
    const editedTask = task ? { ...task, name, description, deadline, progress, important, urgent, finished, photoFilePath } : { name, description, deadline, progress, important, urgent, finished, photoFilePath };
    if (validateTask(editedTask)) {
      saveTask && saveTask(editedTask).then((savedOffline) => {
        if (savedOffline)
          setShowToast(true);
        history.goBack();
      });
    }
  }, [task, saveTask, name, description, deadline, progress, important, urgent, finished, history, photoFilePath]);

  const addPhoto = async () => {
    const photo = await takePhoto();
    setPhoto(photo.webviewPath);
    setPhotoFilePath(photo.filepath);
  };

  log('render');
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>{task ? "Edit Task" : "Create Task"}</IonTitle>
          <IonButtons slot="end">
            <IonButton onClick={handleSave}>
              <IonIcon icon={save} />
            </IonButton>
          </IonButtons>
        </IonToolbar>
      </IonHeader>
      <IonContent className="ion-padding">
        <CreateAnimation
          ref={animationRef}
          duration={2000}
          iterations={Infinity}
          keyframes={[
            { offset: 0, boxShadow: '0 0 20px rgba(0, 0, 0, 0)' },
            { offset: 0.5, boxShadow: '0 0 20px rgba(0, 0, 0, 0.5)' },
            { offset: 1, boxShadow: '0 0 20px rgba(0, 0, 0, 0)' }
          ]}
        >
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
            {showDatetimePicker && <IonDatetime
              presentation="date"
              value={deadline ? deadline.toISOString() : ''}
              onIonChange={e => {
                setDeadline(new Date(e.detail.value as string));
                setShowDatetimePicker(false);
              }}
              onIonCancel={() => setShowDatetimePicker(false)}
            />}
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
            <IonButton onClick={addPhoto}>
              <IonIcon icon={camera} slot="start" />
              Add a photo
            </IonButton>
            {photo && <img src={photo} />}
          </div>
        </CreateAnimation>
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
        <IonToast
          isOpen={showToast}
          onDidDismiss={() => setShowToast(false)}
          message="Changes are saved locally and will be synced when online."
          duration={2000}
          icon={informationOutline}
        />
      </IonContent>
    </IonPage>
  );
};

export default TaskEdit;