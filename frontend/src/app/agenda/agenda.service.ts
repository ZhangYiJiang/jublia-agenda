import { Injectable } from '@angular/core';
import { DashBoardService } from '../dash-board/dash-board.service';
import { Agenda }     from './agenda';

@Injectable()
export class AgendaService {

  constructor (private dashBoardService: DashBoardService) {}

  getAgendaById(id: string): Agenda {
    let agendas = this.dashBoardService.agendas;
    for (var i = 0; i < agendas.length; ++i) {
      if(agendas[i].id === id) {
        return agendas[i];  
      }
    }
  }
}