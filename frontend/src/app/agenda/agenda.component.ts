import { Input, Component, OnInit, ViewContainerRef, ViewEncapsulation, ViewChild, TemplateRef } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { Session } from '../session/session';
import { Agenda } from './agenda';
import { AgendaService } from '../agenda/agenda.service';
import { BoardComponent } from '../board/board.component';
import { GlobalVariable } from '../globals';

import { overlayConfigFactory } from 'angular2-modal';
import { Overlay } from 'angular2-modal';

import {
  VEXBuiltInThemes,
  Modal,
  DialogPreset,
  DialogFormModal,
  DialogPresetBuilder,
  VEXModalContext,
  VexModalModule,
  providers
} from 'angular2-modal/plugins/vex';

@Component({
  selector: 'agenda',
  templateUrl: './agenda.component.html',
  styleUrls: [
    './agenda.component.css'
  ]
})
export class AgendaComponent implements OnInit{
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private agendaService: AgendaService,
    public modal: Modal) { }
  
  agenda: Agenda;
  agendaId: number;
  publicUrl: string;
  clipboardStatus: string;

  @ViewChild('templateRef') public templateRef: TemplateRef<any>;
  @ViewChild('publishRef') public publishRef: TemplateRef<any>;  
  @ViewChild(BoardComponent) public myBoard: BoardComponent;
  
  ngOnInit() {
    this.route.params.forEach((params: Params) => {
        // (+) converts string 'id' to a number
      let id = +params['id'];
      this.agendaId = id;
      this.getAgendaById(id);
    });
    
    this.publicUrl = GlobalVariable.BASE_URL + '/public/agenda/' + this.agendaId;
  }

  updateAgenda(event: any) {
    console.log(event);
    if (typeof event.name === 'string' || 
        typeof event.description === 'string' ||
        typeof event.location === 'string' || 
        typeof event.website === 'string'
    ) {
      this.agendaService.updateAgenda(this.agenda.id, event)
        .subscribe(
          agenda => this.agenda = agenda,
          error => console.log(error)
        );
    } else if (typeof event.duration === 'string') {
      event.duration = +event.duration;
      if(this.isInt(event.duration)) {
        this.agendaService.updateAgenda(this.agenda.id, event)
          .subscribe(
            agenda => {
              this.agenda = agenda;
              this.myBoard.refreshAgenda(agenda);
            },
            error => console.log(error)
          );
      }
    }
  }

  isInt(value: any) {
    return !isNaN(value) && 
           parseInt(value, 10) == value && 
           !isNaN(parseInt(value, 10));
  }

  showAgendaSettings(event: DocumentEvent) {
    this.modal
      .open(this.templateRef, overlayConfigFactory({ isBlocking: false }, VEXModalContext));
  }

  getAgendaById(id: number) {
    this.agendaService.getAgendaById(id).subscribe(
        agenda => this.agenda = agenda,
        error =>  console.log(error)
    );
  }

  openPublishModal() {
    this.modal
      .open(this.publishRef, overlayConfigFactory({ isBlocking: false }, VEXModalContext));
  }

  setPublishedStatus(status: boolean) {
    this.agendaService.setPublished(this.agenda.id, status).subscribe(
      agenda => this.agenda = agenda,
      error =>  console.log(error)
    );
  }
}
