import { Agenda } from './agenda';
import { Session } from '../session/session';

export var SESSIONS: Session[] = 
  [
  <Session>{
      id: '1',
      title: 'session 1',
      venue: 'LT 19',
      order: 1,
      pending: true
  }, 
  <Session>{
    id: '2',
    title: 'session 2',
    order: 2,
    venue: 'LT 19',
    pending: true
  }, 
  <Session>{
    id: '3',
    title: 'session 3',
    venue: 'LT 19',
    order: 3,
    pending: true
  }, 
  <Session>{
    id: '4',
    title: 'session 4',
    venue: 'LT 19',
    order: 4,
    pending: true
  }, 
  <Session>{
    id: '5',
    title: 'lunch',
    venue: 'canteen',
    order: 6,
    start: new Date(2016,5,24,12),
    end: new Date(2016,5,24,13),
    pending: false
  }, 
  <Session>{
    id: '6',
    title: 'lunch',
    venue: 'canteen',
    order: 7,
    start: new Date(2016,7,20,12),
    end: new Date(2016,7,20,13),
    pending: false
  }, 
  <Session>{
    id: '7',
    title: 'opening speech',
    venue: 'auditorium',
    order: 10,
    track: 'Android',
    start: new Date(2016,7,20,8),
    end: new Date(2016,7,20,9),
    pending: false
  }
  ];

export var AGENDAS: Agenda[] = [
  {
    id: '1',
    title: 'sample agenda',
    start: new Date(2016,5,24),
    end: new Date(2016,5,30),
    sessions: SESSIONS,
    tracks: []
  },
  {
    id: '2',
    title: 'another agenda',
    start: new Date(2016,7,20),
    end: new Date(2016,7,30),
    sessions: SESSIONS,
    tracks: ['Android', 'iOS']
  }
];