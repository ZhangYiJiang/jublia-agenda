import { Component, Input, OnInit } from '@angular/core';

import { DragulaService } from 'ng2-dragula/ng2-dragula';

import { Session } from '../session/session';
import {Agenda} from '../agenda/agenda';
import {AgendaService} from '../agenda/agenda.service';

import { DOMUtilService } from '../util/dom.util.service';

@Component({
  selector: 'absolute-column',
  templateUrl: './absolute-column.component.html',
  styleUrls: ['./absolute-column.component.css']
})
export class AbsoluteColumnComponent implements OnInit {
  @Input() sessions: Session[];
  @Input() day: Date;
  @Input() track: string;

  constructor(private dragulaService: DragulaService,
    private agendaService: AgendaService,
    private domUtilService: DOMUtilService) {
    dragulaService.drop.subscribe((value: any) => {
      // console.log(`drop: ${value}`);
      this.onDrop(value.slice(1));
    });
  }

  private onDrop(args: [HTMLElement, HTMLElement]) {
    let [e, el] = args;
    // console.log('drop board');
    // console.log(e);
    // console.log(el);
    // console.log('parent');
    // console.log(e.parentElement);
    let sessionId = parseInt(e.getAttribute('data-session-id'));
    let columnType = el.getAttribute('data-column-type');
    if (columnType === 'absolute') {
      let columnDate = new Date(el.getAttribute('data-date'));
      let columnTrack = el.getAttribute('data-track');
      if (columnDate.toISOString() === this.day.toISOString() && columnTrack === this.track) {
        console.log(sessionId + ' moved to:');
        console.log(columnDate.toLocaleString());
        console.log('moved session:');
        console.log(this.getSessionById(sessionId));
        // for (var i = 0; i < el.children.length; ++i) {
        //   let sessionEl = el.children[i];
        //   console.log(sessionEl.getAttribute('data-session-id'));
        //   if (sessionEl.getAttribute('data-session-id') === sessionId) {
        //     console.log('reached moved session');
        //     break;
        //   }
        //   if (this.domUtilService.hasClass(sessionEl, 'placeholder')) {
        //     console.log('placeholder before session');
        //   } else {
        //     let duration = sessionEl.getAttribute('data-session-duration');
        //     console.log(duration);
        //   }
        // }
      }

    }
  }

  displayedSessions: Session[];

  getSessionById(sessionId: number): Session {
    for (var i = 0; i < this.displayedSessions.length; ++i) {
      if(this.displayedSessions[i].id === sessionId) {
        return this.displayedSessions[i];
      }
    }
    return null;
  }

  ngOnInit(): void {
    this.displayedSessions = this.sessions;
    // console.log(this.displayedSessions);
  }
}
