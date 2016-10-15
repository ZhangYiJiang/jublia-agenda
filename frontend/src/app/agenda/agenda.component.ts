import { Input, Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { Session } from '../session/session';
import { Agenda } from './agenda';
import { AgendaService } from '../agenda/agenda.service';

@Component({
  selector: 'agenda',
  templateUrl: './agenda.component.html',
  styleUrls: ['./agenda.component.css']
})
export class AgendaComponent implements OnInit{
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private agendaService: AgendaService) { }
  
  agenda: Agenda;
  
  ngOnInit() {
    this.route.params.forEach((params: Params) => {
      let id = params['id'];
      this.agendaService.getAgendaById(id).subscribe(
        agenda => this.agenda = agenda,
        error =>  console.log(error)
      );
    });
  }
}
