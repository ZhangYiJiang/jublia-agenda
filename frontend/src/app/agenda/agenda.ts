import { Session } from '../session/session';
import { Track } from '../track/track';
import { Tag } from '../tag/tag';
import { Speaker } from '../speaker/speaker';

export class Agenda {
  id: number;
  title: string;
  start_at: string;
  end_at: string;
  sessions: Session[];
  tracks: Track[];
  speakers: Speaker[];
  tags: Tag[];
  published: boolean;
}
