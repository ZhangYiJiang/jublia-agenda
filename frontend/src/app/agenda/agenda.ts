import { Session } from '../session/session';

export class Agenda {
  id: string;
  title: string;
  start: Date;
  end: Date;
  sessions: Session[];
  tracks: string[];
}