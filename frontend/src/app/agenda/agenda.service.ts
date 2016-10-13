import { Injectable } from '@angular/core';

import { Agenda }     from './agenda';
import { Session }     from '../session/session';
import { AGENDAS }     from './mock-agendas';

@Injectable()
export class AgendaService {
  getAgendas(): Promise<Agenda[]> { 
    return Promise.resolve(AGENDAS);  
  }

  getAgendaById(id: string): Promise<Agenda> {
    for (var i = 0; i < AGENDAS.length; ++i) {
      if(AGENDAS[i].id === id) {
        return Promise.resolve(AGENDAS[i]);  
      }
    }
  }

  updateSession(agendaId: string, newSession: Session) {
    console.log('updating agenda ' + agendaId + ' session ' + newSession.id);
    console.log(JSON.stringify(newSession, null, 4));
  }
}