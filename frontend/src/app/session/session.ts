import { Speaker } from '../speaker/speaker';
import { Track } from '../track/track';

export class Session {
  id: number;
  name: string;
  description: string;
  track: number; // ID of the track
  speakers: Speaker[];
  start_at: number;  //number of minutes since start of the event
  duration: number;  //number of minutes
  url: string;
  venue: string;
  popularity: number;
  //not from api
  placeholder: boolean;
  order: number;
}