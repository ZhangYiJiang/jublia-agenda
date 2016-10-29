export class Session {
  id: number;
  name: string;
  description: string;
  track: number; // ID of the track
  speakers: number[];
  start_at: number;  //number of minutes since start of the event
  duration: number;  //number of minutes
  url: string;
  venue: number;
  popularity: number;
  //not from api
  placeholder: boolean;
  order: number;
}