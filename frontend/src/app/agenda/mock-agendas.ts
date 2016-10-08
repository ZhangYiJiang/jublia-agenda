import { Agenda } from './agenda';
import { Session } from '../session/session';

export var SESSIONS: Session[] = 
  [
  <Session>{
      id: '1',
      title: 'session 1',
      order: 1,
      columnId: '1',
      pending: true
  }, 
  <Session>{
    id: '2',
    title: 'session 2',
    order: 2,
    columnId: '1',
    pending: true
  }
  ];

export var AGENDAS: Agenda[] = [
  {
    id: '1',
    title: 'sample agenda',
    start: new Date(2016,5,24),
    sessions: SESSIONS
  },
  {
    id: '2',
    title: 'another agenda',
    start: new Date(2016,7,20),
    sessions: SESSIONS
  }
];