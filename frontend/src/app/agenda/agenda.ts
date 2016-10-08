import { Session } from '../session/session';

export class Agenda {
  id: string;
  title: string;
  start: Date;
  sessions: Session[]
}