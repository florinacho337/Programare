import React, { memo, useState, useEffect } from 'react';
import { IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonProgressBar, IonText, IonCheckbox, IonLabel } from '@ionic/react';
import { getLogger } from '../core';
import { TaskProps } from './TaskProps';
import './Task.css'; // Import the CSS file

const log = getLogger('Task');

interface TaskPropsExt extends TaskProps {
  onEdit: (_id?: string) => void;
  onToggleFinished: (_id?: string) => void;
}

const Task: React.FC<TaskPropsExt> = ({ _id, name, description, deadline, progress, important, urgent, finished, onEdit, onToggleFinished }) => {
  const [localFinished, setLocalFinished] = useState(finished);
  const pinColor = important && urgent ? 'danger' : important ? 'success' : urgent ? 'secondary' : 'medium';

  useEffect(() => {
    setLocalFinished(finished);
  }, [finished]);

  const handleToggleFinished = () => {
    setLocalFinished(!localFinished);
    onToggleFinished(_id);
  };

  return (
    <IonCard className="task-card" onClick={() => onEdit(_id)}>
      <div className={`pin ${pinColor}`}></div>
      <IonCardHeader>
        <IonCardTitle className="task-title">{name}</IonCardTitle>
        <IonText className="task-deadline">Due to: {new Date(deadline).toLocaleDateString()}</IonText>
      </IonCardHeader>
      <IonCardContent>
        <IonText className="task-description">{description}</IonText>
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
  );
};

export default memo(Task);