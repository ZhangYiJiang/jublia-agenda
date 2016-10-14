import { Session } from '../session/session';
import { Track } from '../track/track';

export class Agenda {
  id: string;
  title: string;
  start_at: string;
  end_at: string;
  sessions: Session[];
  tracks: Track[];
}