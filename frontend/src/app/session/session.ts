import { Speaker } from '../speaker/speaker';
import { Track } from '../track/track';

export class Session {
  id: number;
  name: string;
  desciption: string;
  track: Track;
  speakers: Speaker[];
  start_at: number;  //number of minutes since start of the event
  duration: number;  //number of minutes
  url: string;
  //not from api
  venue: string;
  placeholder: boolean;
  order: number;
}