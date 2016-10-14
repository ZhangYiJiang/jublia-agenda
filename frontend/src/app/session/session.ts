import { Speaker } from '../speaker/speaker';

export class Session {
  id: number;
  name: string;
  desciption: string;
  track: {id: number, name: string, url: string};
  speakers: Speaker[];
  start_at: number;  //number of minutes since start of the event
  duration: number;  //number of minutes
  url: string;
  //not from api
  venue: string;
  placeholder: boolean;
  order: number;
}