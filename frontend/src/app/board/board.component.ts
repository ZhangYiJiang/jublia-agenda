import { Input, Component, OnInit, OnDestroy, ViewContainerRef, ViewEncapsulation, ViewChild, TemplateRef, Renderer, ElementRef } from '@angular/core';
import * as _ from 'lodash';

import { DragulaService } from 'ng2-dragula/ng2-dragula';
import * as moment from 'moment';

import { Session } from '../session/session';
import { Agenda } from '../agenda/agenda';
import { Track } from '../track/track';
import { Tag } from '../tag/tag';
import { Speaker } from '../speaker/speaker';
import { AgendaService } from '../agenda/agenda.service';
import { BoardService } from './board.service';

import { DOMUtilService } from '../util/dom.util.service';
import { overlayConfigFactory } from 'angular2-modal';
import { Overlay } from 'angular2-modal';
import { FormGroup, FormControl, FormBuilder, FormArray, Validators } from '@angular/forms';
import { Observable } from 'rxjs/Rx';

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
  selector: 'board',
  templateUrl: './board.component.html',
  styleUrls: [
  './board.component.css',
  '../session/css/vex.css',
  '../session/css/vex-theme-default.css',
  '../dash-board/dash-board.component.css'
  ],
  encapsulation: ViewEncapsulation.None
})
export class BoardComponent implements OnInit, OnDestroy {
  @ViewChild('templateRef') public templateRef: TemplateRef<any>;
  @Input()
  agenda: Agenda;
  @Input()
  isPublic: boolean;
  @Input()
  token: string;
  @Input()
  interestedSessionIds: number[];

  offsetDate: Date;
  eventDates: Date[];
  eventTracks: Track[];
  eventTags: Tag[];
  eventTagsName: String[];
  eventSpeakers: Speaker[];
  eventSpeakersName: String[];

  allSessions: Session[];
  pendingSessions: Session[];
  nonPendingSessions: Session[];

  dragging: boolean = false;

  hours = ['8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00'];

  private PLACEHOLDER_DURATION: number = 15;

  globalListenFunc: Function;

  constructor(private dragulaService: DragulaService,
    private agendaService: AgendaService,
    private boardService: BoardService,
    private domUtilService: DOMUtilService,
    public modal: Modal,
    private _fb: FormBuilder,
    private elementRef: ElementRef, 
    private renderer: Renderer) {
    dragulaService.dropModel.subscribe((value: any) => {
      // console.log(`drop: ${value}`);
      this.dragging = false;
      this.onDrop(value.slice(1));
    });

    dragulaService.drag.subscribe((value: any) => {
      this.dragging = true;
    });

    dragulaService.cancel.subscribe((value: any) => {
      this.dragging = false;
    });

    dragulaService.setOptions('column', {
      // copy: true,
      // copySortSource: true
      accepts: this.canDropSession.bind(this)
    });
  }

  ngOnDestroy() {
    this.dragulaService.destroy('column');
  }

  canDropSession(el: HTMLElement, target: HTMLElement): boolean {
    // only accept when the slot container is empty
    // or the slot is for pending session
    return this.domUtilService.hasClass(target, 'pending-session-list') 
      || this.canContainerAcceptNewSession(el, target);
  }

  canContainerAcceptNewSession(sessionEl: HTMLElement, target: HTMLElement): boolean {
    if(target.children.length !== 0) {
      return false;
    } else {
      let sessionId = this.domUtilService.getSessionIdFromDOM(sessionEl);
      let containerTrackId = this.domUtilService.getContainerTrack(target);
      let globalStartAt = this.domUtilService.getContainerGlobalStartAt(target);
      return !this.isThereCollision(sessionId, globalStartAt, containerTrackId);
    }
  }

  isThereCollision(draggingSessionId: number, startAt: number, trackId: number): boolean {
    let draggingSession = this.getSessionById(draggingSessionId);
    if(draggingSession == null) {
      console.error('Session not found in board for id: ' + draggingSessionId);
    }
    for (var i = 0; i < this.allSessions.length; i++) {
      // skip pending session
      if(this.allSessions[i].start_at == null) {
        continue;
      }
      // no collision with itself
      if(this.allSessions[i].id !== draggingSessionId
        // same track
        && this.allSessions[i].track === trackId
        // existing session starts before the dragging session ends
        && this.allSessions[i].start_at < (startAt + draggingSession.duration)
        // existing session ends after the dragging session start
        && (this.allSessions[i].start_at + this.allSessions[i].duration) > startAt) {
        console.log('collision with');
        console.log(this.allSessions[i]);
        return true;
      }
    }
    return false;
  }

  onSessionChanged(changedSession: Session) {
    console.log('session changed in board');
    console.log(changedSession);
    this.agendaService.updateSession(this.agenda.id, changedSession);
  }

  onSessionInterestChanged(event: [number, boolean]) {
    console.log('session ' + event[0] + ' changed to ' + event[1]);
    this.agendaService.updateSessionInterest(this.agenda.id, event[0], event[1], this.token);
  }

  onSessionMovedFromPending(sessionFromPending: Session) {
    console.log('session from pending in board');
    console.log(sessionFromPending);
    this.agendaService.updateSession(this.agenda.id, sessionFromPending);
  }

  private onDrop(args: [HTMLElement, HTMLElement]) {
    let [e, el] = args;
    // console.log('drop board');
    // console.log(e);
    // console.log(el);
    let sessionId = e.getAttribute('data-session-id');
    let columnType = el.getAttribute('data-column-type');
    if(columnType === 'relative') {
      this.changeSessionToPending(parseInt(sessionId));
    }
  }

  getSessionsForColumn(columnDate: Date, columnTrack: number): Session[] {
    let sessions:Session[] = [];
    for (let session of this.nonPendingSessions) {
      if (
        //add session to every track if it doesn't have a specific track
        (!session.track || session.track === columnTrack) 
        && this.isOnSameDay(this.addMinToDate(session.start_at, this.agenda.start_at) ,columnDate))
        sessions.push(session);
    }

    return sessions;
  }

  //return the calculated time as a Date
  addMinToDate(minute: number, date: string) {
    let minToMs = 60000;
    let baseMs = new Date(date).getTime();
    return new Date(baseMs + minToMs * minute);
  }

  isOnSameDay(day1: Date, day2: Date) {
    return day1.getUTCFullYear() === day2.getUTCFullYear() 
           && day1.getUTCMonth() === day2.getUTCMonth() 
           && day1.getUTCDate() === day2.getUTCDate();
  }

  changeSessionToPending(sessionId: number) {
    let session: Session = this.getSessionById(sessionId);
    if(session) {
      delete session.start_at;
      console.log('session to pending in board');
      console.log(session);
      this.agendaService.updateSession(this.agenda.id, session);
    } else {
      console.error('Session not found for id=' + sessionId + '.');
    }
  }

  getSessionById(sessionId: number): Session {
    for (var i = 0; i < this.agenda.sessions.length; ++i) {
      if(this.agenda.sessions[i].id === sessionId) {
        return this.agenda.sessions[i];
      }
    }
    return null;
  }

  getEventDates(): Date[] {
    let dates: Date[] = [];
    let endDate: Date;
    // duration has higher precedence of end_date
    console.log(this.agenda);
    if(!(this.agenda.duration == null) && this.agenda.duration > 0) {
      console.log('Using duration: ' + this.agenda.duration);
      endDate = moment.utc(this.agenda.start_at).add(this.agenda.duration - 1, 'd').toDate();
      console.log('End date: ' + endDate.toISOString());
    } else if(this.agenda.end_at == null) {
      console.log('No duration or end date, use 3 days default.');
      // initial deafult duration 3 days for empty agenda
      // endDate is the last day of the event
      endDate = moment.utc(this.agenda.start_at).add(2, 'd').toDate();
    } else {
      endDate = moment.utc(this.agenda.end_at).toDate();  
      console.log('Using end date: ' + endDate.toISOString());
    }
    let tempDate: Date = moment.utc(this.agenda.start_at).toDate();
    
    while (tempDate <= endDate) {
      // create cloned Date to avoid mutating start date
      dates.push(new Date(tempDate.getTime()));
      tempDate.setDate(tempDate.getDate() + 1);
    }
    return dates;
  }

  getEventTracks(): Track[] {
    if (!this.agenda.tracks || this.agenda.tracks.length === 0) {
      return [];
    } else {
      return this.agenda.tracks;
    }
  }

  getEventTags(): Tag[] { // using tracks for testing
    // if (!this.agenda.tags || this.agenda.tags.length === 0) {
    //   return [];
    // } else {
    //   return this.agenda.tags;
    // }
    if (!this.agenda.tracks || this.agenda.tracks.length === 0) {
      return [];
    } else {
      return this.agenda.tracks;
    }  
  }

  getEventTagsName(): String[] {
    if (!this.eventTags || this.eventTags.length === 0) {
      return [];
    } else {
      return this.eventTags.map(function(tag) {return tag.name;});
    }
  }

  getEventSpeakers(): Speaker[] {
    if (!this.agenda.speakers || this.agenda.speakers.length === 0) {
      return [];
    } else {
      return this.agenda.speakers;
    }
  }

  getEventSpeakersName(): String[] {
    if (!this.eventSpeakers || this.eventSpeakers.length === 0) {
      return [];
    } else {
      return this.eventSpeakers.map(function(speaker) {return speaker.name;});
    }
  }

  sessionForm: FormGroup;
  formMsg: string;
  options = {
    placeholderTags: "+ tag",
    secondaryPlaceholderTags: "Enter a custom tag",
    placeholderSpeakers: "+ speaker",
    secondaryPlaceholderSpeakers: "Add an existing speaker"
  }

  ngOnInit(): void {
    this.offsetDate = new Date(this.agenda.start_at);
    this.eventDates = this.getEventDates();
    this.eventTracks = this.getEventTracks();
    this.eventTags = this.getEventTags();
    this.eventTagsName = this.getEventTagsName();
    this.eventSpeakers = this.getEventSpeakers();
    this.eventSpeakersName = this.getEventSpeakersName();
    if(this.agenda.sessions == null) {
      this.agenda.sessions = [];
    }
    this.allSessions = this.agenda.sessions;
    let partioned = _.partition(this.allSessions, function(o:Session){return o.hasOwnProperty('start_at')});
    this.pendingSessions = partioned[1];
    this.nonPendingSessions = partioned[0];
  }

  refreshAgenda(newAgenda: Agenda) {
    this.agenda = newAgenda;
    this.eventDates = this.getEventDates();
  }

  createSessionModal() {
    console.log("session modal");
    this.sessionForm = this._fb.group({
      name: ['', [<any>Validators.required]],
      description: [''],
      duration: ['', [<any>Validators.required]],
      existingSpeakers: [[]],
      newSpeakers: this._fb.array([]),
      tags: [[]]
    });
    this.formMsg = "";
    this.modal.open(this.templateRef, overlayConfigFactory({ isBlocking: false }, VEXModalContext));
  }

  onSelected() {
    let docs = document.getElementsByTagName("ng2-dropdown-menu");
    for (let i = 0; i < docs.length; i++) {
      document.getElementsByTagName("ng2-dropdown-menu")[i].addEventListener('click', function(event: any) {
        event.stopPropagation();
      });  
    }
  }

  initSpeaker() {
    return this._fb.group({
        name: ['', Validators.required],
        company: ['', Validators.required],
        position: ['', Validators.required],
        email: ['', Validators.required],
        phone_number: [''],
        company_description: [''],
        company_url: ['']
    });
  }

  addSpeaker() {
    const control = <FormArray>this.sessionForm.controls['newSpeakers'];
    control.push(this.initSpeaker());
  }

  removeSpeaker(i: number) {
    const control = <FormArray>this.sessionForm.controls['newSpeakers'];
    control.removeAt(i);
  }

  submitSessionForm(isValid: boolean) {
    if (!isValid) { 
      this.formMsg = "Please fill in all required information.";
      return;
    }
    let observables: Observable<any>[] = [];
    if (!this.sessionForm.value.existingSpeakers) {
      this.sessionForm.value.existingSpeakers = [];
    }
    for (let speaker of this.sessionForm.value.newSpeakers) {
      observables.push(this.boardService.createSpeaker(this.agenda.id, speaker.name, speaker.company, speaker.position, speaker.email, speaker.phone_number, speaker.company_description, speaker.company_url));
    }
    if (!this.sessionForm.value.tags) {
      this.sessionForm.value.tags = [];
    }
    let newTagsCount: number = 0;
    // for (let tag of this.sessionForm.value.tags) {
    //   if (!this.eventTagsName.some(function(existingTag) {return existingTag === tag})) {
    //     observables.push(this.boardService.createTag(this.agenda.id, tag));
    //     newTagsCount += 1;
    //   }
    // }
    console.log(this.sessionForm.value);
    if (observables.length > 0) {
      Observable.forkJoin(observables).subscribe(
        data => {
          let newSpeakersCount: number = this.sessionForm.value.newSpeakers.length;
          for (let i = 0; i < newSpeakersCount; i++) {
            console.log('new speaker created: ' + data[i].name);
            this.eventSpeakers.push(data[i]);
            this.sessionForm.value.existingSpeakers.push(data[i].name);
          }
          for (let i = newSpeakersCount; i < newSpeakersCount+newTagsCount; i++) {
            console.log('new tag created: ' + data[i].name);
            this.eventTags.push(data[i]);
          }
          this.createSession();
        },
        error =>  this.formMsg = <any>error
      );
    }
    else {
      this.createSession();
    }
  }

  createSession() {
    let speakers: Speaker[] = this.eventSpeakers;
    let tags: Tag[] = this.eventTags;
    function getId(name: string, lookup: any) {
      for (let item of lookup) {
        if (item.name === name) {
          return item.id;
        }
      }
    }
    let speakersId: number[] = this.sessionForm.value.existingSpeakers.map(function(name: string) {return getId(name, speakers)});
    let tagsId: number[] = this.sessionForm.value.tags.map(function(name: string) {return getId(name, tags)});
    console.log(speakersId);
    console.log(tagsId);
    this.boardService.createSession(this.agenda.id, this.sessionForm.value.name, this.sessionForm.value.description, 
                                    this.sessionForm.value.duration, speakersId, tagsId).subscribe(
      data => { 
        this.formMsg = 'New session created!';
        this.allSessions.push(data);
        this.pendingSessions.push(data);
      },
      error =>  this.formMsg = <any>error
    );
  }
}
