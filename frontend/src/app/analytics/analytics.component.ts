import { Input, Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { Session } from '../session/session';
import { Agenda } from '../agenda/agenda';
import { AgendaService } from '../agenda/agenda.service';

@Component({
  selector: 'analytics',
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.css']
})
export class AnalyticsComponent implements OnInit{
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private agendaService: AgendaService) { }
  
  agenda: Agenda;
  
  ngOnInit() {
    this.route.params.forEach((params: Params) => {
      let id = params['id'];
      this.getAgendaById(id);
    });
  }

  getAgendaById(id: number) {
    this.agendaService.getAgendaById(id).subscribe(
        agenda => {if (agenda.published) {this.agenda = agenda}},
        error =>  console.log(error)
    );
  }
}
