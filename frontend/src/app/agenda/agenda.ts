import { Session } from '../session/session';

export class Agenda {
  id: string;
  title: string;
  start_at: string;
  end_at: string;
  sessions: Session[];
  tracks: string[];
}