import React, { memo, useState, useEffect, useRef } from 'react';
import { IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonProgressBar, IonText, IonCheckbox, IonLabel, CreateAnimation, IonImg, IonCol } from '@ionic/react';
import { getLogger } from '../core';
import { TaskProps } from './TaskProps';
import './Task.css'; // Import the CSS file
import { usePhotoGallery } from '../hooks/usePhotoGallery';

const log = getLogger('Task');

interface TaskPropsExt extends TaskProps {
  onEdit: (_id?: string) => void;
  onToggleFinished: (_id?: string) => void;
}

const Task: React.FC<TaskPropsExt> = ({ _id, name, description, deadline, progress, important, urgent, finished, photoFilePath, onEdit, onToggleFinished }) => {
  const [localFinished, setLocalFinished] = useState(finished);
  const [displayedPhoto, setDisplayedPhoto] = useState<string>();
  const pinColor = important && urgent ? 'danger' : important ? 'success' : urgent ? 'secondary' : 'medium';
  const animationRef = useRef<CreateAnimation>(null);
  const { loadPhoto } = usePhotoGallery();

  useEffect(() => {
    if (photoFilePath) {
      loadPhoto(photoFilePath).then((photo) => setDisplayedPhoto(photo.webviewPath));
    }
  }, [photoFilePath]);

  useEffect(() => {
    setLocalFinished(finished);
  }, [finished]);

  const handleToggleFinished = () => {
    setLocalFinished(!localFinished);
    onToggleFinished(_id);
  };

  useEffect(() => {
    animationRef.current?.animation.play();
  }, []);

  return (
    <CreateAnimation
      ref={animationRef}
      duration={600}
      iterations={2}
      keyframes={[
        { offset: 0, transform: 'scale(1)', opacity: '1' },
        { offset: 0.5, transform: 'scale(1.1)', opacity: '0.7' },
        { offset: 1, transform: 'scale(1)', opacity: '1' }
      ]}
    >
      <IonCard className="task-card" onClick={() => onEdit(_id)}>
        <div className={`pin ${pinColor}`}></div>
        <IonCardHeader>
          <IonCardTitle className="task-title">{name}</IonCardTitle>
          <IonText className="task-deadline">Due to: {new Date(deadline).toLocaleDateString()}</IonText>
        </IonCardHeader>
        <IonCardContent>
          <IonText className="task-description">{description}</IonText>
          {displayedPhoto && <img src={displayedPhoto} />}
          <div className="progress-container">
            <IonProgressBar value={progress / 100} className="progress-bar"></IonProgressBar>
            <IonText>{progress}%</IonText>
          </div>
          <div className="finished">
            <IonLabel className="finished-label">Finished</IonLabel>
            <IonCheckbox checked={localFinished} onIonChange={handleToggleFinished} />
          </div>
        </IonCardContent>
      </IonCard>
    </CreateAnimation>
  );
};

export default memo(Task);