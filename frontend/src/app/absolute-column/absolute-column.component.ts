import { Component, Input, OnInit } from '@angular/core';

import { DragulaService } from 'ng2-dragula/ng2-dragula';
import * as _ from 'lodash';
import * as moment from 'moment';

import { Session } from '../session/session';
import { Agenda } from '../agenda/agenda';
import { Track } from '../track/track';
import { AgendaService } from '../agenda/agenda.service';

import { DOMUtilService } from '../util/dom.util.service';

@Component({
  selector: 'absolute-column',
  templateUrl: './absolute-column.component.html',
  styleUrls: ['./absolute-column.component.css']
})
export class AbsoluteColumnComponent implements OnInit {
  @Input() sessions: Session[];
  @Input() day: Date;
  @Input() track: Track;
  @Input() offsetDate: Date;

  private PLACEHOLDER_DURATION: number = 15;
  private DEFAULT_DAY_START_OFFSET_MIN: number = 8 * 60; // default start time for column is 8AM
  private dayStartOffsetMin: number;

  displayedSessions: Session[];

  constructor(private dragulaService: DragulaService,
    private agendaService: AgendaService,
    private domUtilService: DOMUtilService) {
    dragulaService.dropModel.subscribe((value: any) => {
      // console.log(`drop: ${value}`);
      this.onDrop(value.slice(1));
    });
  }

  private onDrop(args: [HTMLElement, HTMLElement]) {
    let [e, el] = args;
    let sessionId = parseInt(e.getAttribute('data-session-id'));
    let columnType = el.getAttribute('data-column-type');
    if (columnType === 'absolute') {
      let columnDate = new Date(el.getAttribute('data-date'));
      let columnTrackId = +el.getAttribute('data-track-id');
      if (columnDate.toISOString() === this.day.toISOString() && columnTrackId === this.track.id) {
        console.log(sessionId + ' moved to:');
        console.log(columnDate.toLocaleString());
        console.log('moved session:');
        console.log(this.getSessionById(sessionId));
        console.log(this.offsetDate.toISOString());
        console.log(this.day.toISOString());

        let duration: number = 0;
        for (var i = 0; i < this.displayedSessions.length; ++i) {
          let session: Session = this.displayedSessions[i];
          if(session.id === sessionId) {
            console.log('reached moved session');
            break;
          } else if(session.placeholder) {
            console.log('reached placeholder');
            duration += this.PLACEHOLDER_DURATION;
          } else {
            duration += session.duration;
          }
        }
        console.log('totoal duration: ' + duration);
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

  // Get start minutes of session relative to start of the day
  getRelativeStartMin(session: Session): number {
    console.log(session);
    let offsetMins = moment(this.day).diff(moment(this.offsetDate), 'minutes', true);
    if(offsetMins % 60 !== 0) {
      console.error('offset date and current date diff is not exact multiple of days');
    }
    return session.start_at - offsetMins - this.dayStartOffsetMin;
  }

  getSessionById(sessionId: number): Session {
    for (var i = 0; i < this.displayedSessions.length; ++i) {
      if(this.displayedSessions[i].id === sessionId) {
        return this.displayedSessions[i];
      }
    }
    return null;
  }

  addPlaceHolderSessions(rawSessions: Session[]): Session[] {
    let newSessions: Session[] = [];
    let lastSessionMins: number = 0;
    for (var i = 0; i < rawSessions.length; i++) {
      let relativeStartMins = this.getRelativeStartMin(rawSessions[i]);
      if(relativeStartMins < 0) {
        console.error('Start minutes relative to start of the day smaller than zero.');
      }
      if(relativeStartMins - lastSessionMins < 0) {
        console.error('Start minutes relative to last session smaller than zero.');
      }
      // round down number of placeholders
      let noOfPlaceholders = Math.floor((relativeStartMins - lastSessionMins) / this.PLACEHOLDER_DURATION);
      console.log('relativeStartMins: ' + relativeStartMins);
      console.log('noOfPlaceholders: ' + noOfPlaceholders);
      for (var j = 0; j < noOfPlaceholders; ++j) {
        newSessions.push(<Session>{
          placeholder: true
        })
      }
      newSessions.push(rawSessions[i]);
      lastSessionMins = relativeStartMins + rawSessions[i].duration;
    }
    // placeholders after the last session
    // allow 4 hours
    for (var i = 0; i < (60 / this.PLACEHOLDER_DURATION * 4); ++i) {
      newSessions.push(<Session>{
        placeholder: true
      })
    }
    return newSessions;
  }

  ngOnInit(): void {
    if(this.sessions.length > 0) {
      let firstSessionMins = this.getRelativeStartMin(this.sessions[0]);
      if(firstSessionMins < this.DEFAULT_DAY_START_OFFSET_MIN) {
        console.error('Earliest session before 8AM, session before 8AM will be hidden.');
      }
    }
    this.dayStartOffsetMin = this.DEFAULT_DAY_START_OFFSET_MIN;
    let sortedSessions = _.sortBy(this.sessions, ['start_at']);
    this.displayedSessions = this.addPlaceHolderSessions(sortedSessions);
    // console.log(this.displayedSessions);
  }
}
