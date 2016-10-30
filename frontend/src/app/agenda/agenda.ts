import { Session } from '../session/session';
import { Track } from '../track/track';
import { Category } from '../category/category';
import { Speaker } from '../speaker/speaker';
import { Venue } from '../venue/venue';

export class Agenda {
  id: number;
  name: string;
  location: string;
  start_at: string;
  end_at: string;
  duration: number; // number of days
  website: string;
  sessions: Session[];
  tracks: Track[];
  speakers: Speaker[];
  categories: Category[];
  session_venues: Venue[];
  published: boolean;
}
