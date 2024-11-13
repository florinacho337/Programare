import React, { useEffect, useState } from 'react';
import { IonToast, IonIcon } from '@ionic/react';
import { Network } from '@capacitor/network';
import { wifi, alert } from 'ionicons/icons';

const NetworkStatus: React.FC = () => {
  const [networkStatus, setNetworkStatus] = useState<boolean>(true);
  const [showToast, setShowToast] = useState<boolean>(false);

  useEffect(() => {
    const getStatus = async () => {
      const status = await Network.getStatus();
      setNetworkStatus(status.connected);
    };

    const addNetworkListener = () => {
      Network.addListener('networkStatusChange', (status) => {
        setNetworkStatus(status.connected);
        setShowToast(true);
      });
    };

    getStatus();
    addNetworkListener();

    return () => {
      Network.removeAllListeners();
    };
  }, []);

  return (
    <>
      <IonToast
        isOpen={showToast}
        onDidDismiss={() => setShowToast(false)}
        message={networkStatus ? 'You are online' : 'You are offline'}
        duration={2000}
        icon={networkStatus ? wifi : alert}
      />
    </>
  );
};

export default NetworkStatus;