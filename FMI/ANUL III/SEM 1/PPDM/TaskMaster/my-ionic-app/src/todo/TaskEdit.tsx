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
  CreateAnimation,
  IonModal,
  createAnimation
} from '@ionic/react';
import { save, informationOutline, camera, location as loc } from 'ionicons/icons';
import { getLogger } from '../core';
import { TaskContext } from './TaskProvider';
import { RouteComponentProps } from 'react-router';
import { TaskProps } from './TaskProps';
import './TaskEdit.css';
import { usePhotoGallery } from '../hooks/usePhotoGallery';
import { Geolocation } from '@capacitor/geolocation';
import MyMap from '../components/MyMap';

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
  const [location, setLocation] = useState<{ lat: number; lng: number } | undefined>(undefined);
  const [showMapModal, setShowMapModal] = useState(false);
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
      setLocation(task.location);
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
    const editedTask = task ? { ...task, name, description, deadline, progress, important, urgent, finished, photoFilePath, location } : { name, description, deadline, progress, important, urgent, finished, photoFilePath, location };
    if (validateTask(editedTask)) {
      saveTask && saveTask(editedTask).then((savedOffline) => {
        if (savedOffline)
          setShowToast(true);
        history.goBack();
      });
    }
  }, [task, saveTask, name, description, deadline, progress, important, urgent, finished, history, photoFilePath, location]);

  const addPhoto = async () => {
    const photo = await takePhoto();
    setPhoto(photo.webviewPath);
    setPhotoFilePath(photo.filepath);
  };

  const selectLocation = async () => {
    const coordinates = await Geolocation.getCurrentPosition();
    setLocation({ lat: coordinates.coords.latitude, lng: coordinates.coords.longitude });
  };

  const handleLocationSelect = (lat: number, lng: number) => {
    setLocation({ lat, lng });
  };

  const handleShowMap = () => {
    setShowMapModal(true);
  }

  const handleCloseMap = () => {
    setShowMapModal(false);
  }

  const enterAnimation = (baseEl: HTMLElement) => {
    const root = baseEl.shadowRoot || baseEl;
  
    const backdropAnimation = createAnimation()
      .addElement(root.querySelector('ion-backdrop')!)
      .fromTo('opacity', '0.01', 'var(--backdrop-opacity)');
  
    const wrapperAnimation = createAnimation()
      .addElement(root.querySelector('.modal-wrapper')!)
      .keyframes([
        { offset: 0, transform: 'translateX(100%)', opacity: '0' },
        { offset: 1, transform: 'translateX(0)', opacity: '1' },
      ]);
  
    return createAnimation()
      .addElement(baseEl)
      .easing('ease-out')
      .duration(500)
      .addAnimation([backdropAnimation, wrapperAnimation]);
  };
  
  const leaveAnimation = (baseEl: HTMLElement) => {
    const root = baseEl.shadowRoot || baseEl;
  
    const backdropAnimation = createAnimation()
      .addElement(root.querySelector('ion-backdrop')!)
      .fromTo('opacity', 'var(--backdrop-opacity)', '0.01');
  
    const wrapperAnimation = createAnimation()
      .addElement(root.querySelector('.modal-wrapper')!)
      .keyframes([
        { offset: 0, transform: 'translateX(0)', opacity: '1' },
        { offset: 1, transform: 'translateX(-100%)', opacity: '0' },
      ]);
  
    return createAnimation()
      .addElement(baseEl)
      .easing('ease-in')
      .duration(500)
      .addAnimation([backdropAnimation, wrapperAnimation]);
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
            <div className="location-container">
              <IonButton onClick={handleShowMap}>
                <IonIcon icon={loc} slot="start" />
                Select Location
              </IonButton>
              {location && (
                <IonText>
                  Location set!
                </IonText>
              )}
            </div>
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
        <IonModal isOpen={showMapModal} onDidDismiss={() => setShowMapModal(false)} enterAnimation={enterAnimation} leaveAnimation={leaveAnimation}>
          <MyMap onLocationSelect={handleLocationSelect} showExistingMarkers={false} actualLocation={location}/>
          <IonButton onClick={handleCloseMap}>Close Map</IonButton>
        </IonModal>
      </IonContent>
    </IonPage>
  );
};

export default TaskEdit;