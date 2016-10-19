import { Session } from '../session/session';
import { Track } from '../track/track';

export class Agenda {
  id: number;
  title: string;
  start_at: string;
  end_at: string;
  sessions: Session[];
  tracks: Track[];
  speakers: any[];
  published: boolean;
}