import { GoogleMap } from '@capacitor/google-maps';
import { useRef, useEffect } from 'react';
import { TaskProps } from '../todo/TaskProps';
import { Geolocation } from '@capacitor/geolocation';
import './MyMap.css';
import { MAPS_API_KEY } from '../../mapsApiKey';

interface MyMapProps {
  tasks?: TaskProps[];
  onLocationSelect?: (latitude: number, longitude: number) => void;
  showExistingMarkers?: boolean;
  actualLocation?: { lat: number, lng: number };
  enterTask?: (_id?: string) => void;
}

const MyMap: React.FC<MyMapProps> = ({ tasks = [], onLocationSelect, showExistingMarkers = true, actualLocation, enterTask }) => {
  const mapRef = useRef<HTMLElement>();
  const currentMarkerIdRef = useRef<string | null>(null);
  const markerClickHandledRef = useRef<boolean>(false);
  let firstId = '-1';
  let firstMarker = true;
  let newMap: GoogleMap;

  async function createMap() {
    if (!mapRef.current) return;

    const coordinates = await Geolocation.getCurrentPosition();

    newMap = await GoogleMap.create({
      id: 'my-cool-map',
      element: mapRef.current,
      apiKey: MAPS_API_KEY,
      config: {
        center: {
          lat: coordinates.coords.latitude,
          lng: coordinates.coords.longitude
        },
        zoom: 12
      }
    });

    if (showExistingMarkers) {
      tasks.forEach(async (task) => {
        if (task.location) {
          const markerId = await newMap.addMarker({
            coordinate: {
              lat: task.location.lat,
              lng: task.location.lng
            },
            title: task.name,
            snippet: task.description
          });

          if (enterTask) {
            newMap.setOnMarkerClickListener((marker) => {
              if (!markerClickHandledRef.current && markerId === marker.markerId) {
                markerClickHandledRef.current = true;
                console.log('Marker clicked coords: ', marker.latitude, marker.longitude);
                console.log('Task coords: ', task.location?.lat, task.location?.lng);
                enterTask(task._id);
                setTimeout(() => {
                  markerClickHandledRef.current = false;
                }, 1000); // Reset the flag after 1 second
              }
            });
          }
        }
      });
    }

    if (actualLocation) {
      const markerId = await newMap.addMarker({
        coordinate: {
          lat: actualLocation.lat,
          lng: actualLocation.lng
        },
        title: 'Actual Location',
        snippet: 'This is the actual location'
      });

      firstId = markerId;
      currentMarkerIdRef.current = markerId;
    }

    if (onLocationSelect && !showExistingMarkers) {
      newMap.setOnMapClickListener(async (event) => {
        const { latitude, longitude } = event;

        // Remove the existing marker if it exists
        if (currentMarkerIdRef.current) {
          if (firstMarker && Number.parseInt(currentMarkerIdRef.current) != Number.parseInt(firstId)){
            firstMarker = false;
            await newMap.removeMarker(firstId);
          }
          console.log('Removing existing marker ', currentMarkerIdRef.current);
          await newMap.removeMarker(currentMarkerIdRef.current);
          currentMarkerIdRef.current = null;
        }

        // Add a new marker
        const markerId = await newMap.addMarker({
          coordinate: {
            lat: latitude,
            lng: longitude
          },
          title: 'New Location',
          snippet: 'This is the selected location'
        });

        // Update the current marker ID ref
        currentMarkerIdRef.current = markerId;
        console.log('New marker set: ', markerId);

        onLocationSelect(latitude, longitude);
      });
    }
  }

  useEffect(() => {
    createMap();
  }, []);

  return (
    <div className="component-wrapper">
      <capacitor-google-map ref={mapRef} style={{
        display: 'flex',
        width: '100%',
        height: '100%'
      }}></capacitor-google-map>
    </div>
  );
}

export default MyMap;