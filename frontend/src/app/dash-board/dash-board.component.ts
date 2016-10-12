import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { Agenda } from '../agenda/agenda';
import { AgendaService } from '../agenda/agenda.service';

@Component({
  selector: 'dash-board',
  templateUrl: './dash-board.component.html',
  styleUrls: ['./dash-board.component.css']
})
export class DashBoardComponent {
  constructor(
  private router: Router,
  private agendaService: AgendaService) { }

  agendas: Agenda[] = [];
  ngOnInit() {
    this.agendaService.getAgendas()
    .then((agendas: Agenda[]) => {
      this.agendas.push(...agendas);
    })
  }

  onSelect(agenda: Agenda) {
    this.router.navigate(['/agenda', agenda.id]);
  }
}
