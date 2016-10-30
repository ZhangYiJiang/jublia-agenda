import { Input, Component, OnInit, ViewContainerRef, ViewEncapsulation, ViewChild, TemplateRef, EventEmitter, Output } from '@angular/core';

import { Session } from '../session/session';
import { Agenda } from '../agenda/agenda';
import { Speaker } from '../speaker/speaker';
import { Venue } from '../venue/venue';
import { Tag} from '../tag/tag';
import { BoardService } from '../board/board.service';

import { overlayConfigFactory } from 'angular2-modal';
import { Overlay } from 'angular2-modal';

import * as moment from 'moment';
import * as _ from 'lodash';

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
  selector: 'my-session',
  templateUrl: './session.component.html',
  styleUrls: [
    './session.component.css',
    './css/vex.css',
    './css/vex-theme-default.css',
  ],
  encapsulation: ViewEncapsulation.None
})
export class SessionComponent implements OnInit {
  constructor(public modal: Modal,
    private boardService: BoardService) {
  }
  @ViewChild('templateRef') public templateRef: TemplateRef<any>;
  @Input() session: Session;
  @Input() offsetDate: Date;
  @Input() agenda: Agenda;
  @Input() isPublic: boolean;

  @Input() token: string;

  @Input() interested: boolean;

  interestedButtonText: string;

  @Output() onSessionEdited = new EventEmitter<Session>();
  @Output() onSessionDeleted = new EventEmitter<Session>();
  @Output() onSessionInterestEdited = new EventEmitter<[number, boolean]>();
  @Output() onSpeakerEdited = new EventEmitter<Speaker>();
  @Output() onVenueEdited = new EventEmitter<Venue>();

  speakersObj = {};
  trackObj = {};
  sessionTagsName: string[] = [];
  eventTags: Tag[] = [];
  eventTagsName: string[] = [];

  HEIGHT_PER_15_MINS = 20; // px
  VERTICAL_MARGIN = 4;

  height: number;
  red: number;
  green: number;
  blue: number;
  
  getVenue(): Venue {
    return _.find(this.agenda.session_venues, {id: this.session.venue});
  }

  updateInterest() {
    this.interested = !this.interested;
    this.updateInterestButtonText();
    this.onSessionInterestEdited.emit([this.session.id, this.interested]);
  }

  adjustSessionDuration(mins: number) {
    console.log(mins);
    let newDuration = this.session.duration + mins;
    if(newDuration > 0) {
      this.updateSession({
        duration: newDuration
      });  
    }
  }

  confirmDelete(dialogRef: any) {
    console.log('confirm delete');
    let dialog = this.modal.confirm()
      .message('Confirm delete?')
      .okBtn('Delete')
      .cancelBtn('Cancel')
      .open();
    dialog.then((resultPromise) => {
      return resultPromise.result.then((result) => {
        this.deleteSession();
        dialogRef.close(true);
      }, () => {});
    });
  }

  deleteSession() {
    this.onSessionDeleted.emit(this.session);
  }

  updateSession(event: any) {
    console.log(event);
    if(typeof event.description === 'string') {
      console.log(this.session);
      this.session.description = event.description;
      this.onSessionEdited.emit(this.session);
    } else if(typeof event.name === 'string') {
      this.session.name = event.name;
      this.onSessionEdited.emit(this.session);
    } else if(typeof event.duration === 'string' || typeof event.duration === 'number') {
      event.duration = +event.duration;
      if (this.isInt(event.duration)) {
        this.session.duration = event.duration;
        this.onSessionEdited.emit(this.session);
        this.updateHeight();
      }
    }
  }

  updateSessionSpeaker(speakerId: number) {
    this.session.speakers = _.without(this.session.speakers, speakerId);
    this.onSessionEdited.emit(this.session);
  }

  updateSpeaker(event: any, speakerId: number) {
    let newSpeaker = this.agenda.speakers.filter(function(speaker) {return speaker.id === speakerId})[0];
    console.log(event);
    if(typeof event.name === 'string') {
      newSpeaker.name = event.name;
      this.onSpeakerEdited.emit(newSpeaker);
    } else if(typeof event.position === 'string') {
      newSpeaker.position = event.position;
      this.onSpeakerEdited.emit(newSpeaker);
    } else if(typeof event.email === 'string') {
      newSpeaker.email = event.email;
      this.onSpeakerEdited.emit(newSpeaker);
    } else if(typeof event.phone_number === 'string') {
      newSpeaker.phone_number = event.phone_number;
      this.onSpeakerEdited.emit(newSpeaker);
    }
  }

  updateVenue(event: any) {
    console.log(event);
    let newVenue = this.getVenue();
    if(typeof event.unit === 'string') {
      newVenue.unit = event.unit;
      this.onVenueEdited.emit(newVenue);
    }
  }

  removeTag(name: string) {
    let tagId: number = _.find(this.eventTags, {name}).id;
    let defaultCategoryId: number = this.agenda.categories[0].id;
    this.session.categories[defaultCategoryId] = _.without(this.session.categories[defaultCategoryId], tagId);
    this.session.tags = this.session.categories[defaultCategoryId]; // api takes in an array of tag ids
    this.onSessionEdited.emit(this.session);
  }

  addTag(name: string) {
    let defaultCategoryId: number = this.agenda.categories[0].id;
    if (!this.session.categories) {
      this.session.categories = {};
      this.session.categories[defaultCategoryId] = [];
    }
    let tagId: number;
    if (_.includes(this.eventTagsName, name)) {
      tagId = _.find(this.eventTags, {name}).id;
      this.session.categories[defaultCategoryId].push(tagId);
      this.session.tags = this.session.categories[defaultCategoryId]; // api takes in an array of tag ids
      this.onSessionEdited.emit(this.session);
    }
    else {
      this.boardService.createTag(this.agenda.id, defaultCategoryId, name).subscribe(
        (data: Tag) => {
          console.log('new tag created: ' + data.name);
          tagId = data.id;
          this.session.categories[defaultCategoryId].push(tagId);
          this.session.tags = this.session.categories[defaultCategoryId]; // api takes in an array of tag ids
          this.onSessionEdited.emit(this.session);
          this.eventTags.push(data);
          this.eventTagsName.push(data.name);
        },
        error => {
          console.log(error);
        }
      );
    }
  }

  isInt(value: any) {
    return !isNaN(value) && 
           parseInt(value, 10) == value && 
           !isNaN(parseInt(value, 10));
  }

  clicked(event: DocumentEvent) {
    this.eventTags = this.getEventTags();
    this.eventTagsName = this.getEventTagsName();
    this.sessionTagsName = _.values(_.values(this.session.categories)[0])
        .map((id: number) => _.find(this.eventTags, {id}).name);
    this.modal.open(
      this.templateRef, 
      overlayConfigFactory({ isBlocking: false }, VEXModalContext)
    ).then(dialog => {
      // Stop click events from the dropdown menu created by the tag inputs from propagating 
      // to document body, which causes weird issues with the modal widget
      // We're using setImmediate here because we need to wait for the widgets in the modal to be 
      // rendered first
      setImmediate(() => {
        _.each(document.getElementsByTagName("ng2-dropdown-menu"), el => {
          el.addEventListener('click', evt => evt.stopPropagation());
        });
      });
      
      // Clean up dropdown menus that were left behind by the widget
      dialog.onDestroy.subscribe(() => {
        // querySelectorAll uses a frozen NodeList
        _.each(document.querySelectorAll("ng2-dropdown-menu"), el => {
          el.parentNode.removeChild(el);
        });
      });
    });
  }

  getDisplayedDate(): string {
    if (this.session.start_at == null) {
      return '';
    }
    
    const startMs = this.offsetDate.getTime() + 60000 * this.session.start_at;
    return moment(startMs).utc().format("ddd, MMMM Do");
  }

  getDisplayedTime(): string {
    if (this.session.start_at == null) {
      return '';
    }
    
    const startMs = this.offsetDate.getTime() + 60000 * this.session.start_at;
    const startDate = new Date(startMs);
    const endDate = new Date(startMs + 60000 * this.session.duration);
    return `${this.getFormattedTime(startDate)}–${this.getFormattedTime(endDate)}`;
  }

  getFormattedTime(date: Date): string {
    return date.getUTCHours() + ':' + (date.getUTCMinutes() < 10 ? '0' : '') + date.getUTCMinutes();
  }

  getAltFormattedTime(date: Date): string {
    return moment(date).utc().format("hA");
  }

  updateInterestButtonText() {
    if(this.interested) {
      this.interestedButtonText = 'Bookmarked. Click to remove';
    } else {
      this.interestedButtonText = 'Bookmark This Session';
    }
  }

  updateHeight() {
    this.height = Math.ceil(this.session.duration / 15) * this.HEIGHT_PER_15_MINS - this.VERTICAL_MARGIN;
  }

  getEventTags(): Tag[] { // only from first (default) category for now
    if (!this.agenda.categories[0].tags || this.agenda.categories[0].tags.length === 0) {
      return [];
    } else {
      return this.agenda.categories[0].tags;
    }
  }

  getEventTagsName(): string[] {
    if (!this.eventTags || this.eventTags.length === 0) {
      return [];
    } else {
      return this.eventTags.map(tag => tag.name);
    }
  }

  ngOnInit(): void {
    // TODO: move this logic up to agenda/board component to avoid repeated operations
    this.speakersObj = _.keyBy(this.agenda.speakers, 'id');
    this.trackObj = _.keyBy(this.agenda.tracks, 'id');

    this.updateInterestButtonText();

    if (this.session.start_at != null) {
      this.updateHeight();
    }

    let popularityRatio = 0;
    
    if (this.isPublic) {
      popularityRatio = this.session.popularity / 10; // TODO: divide by highest popularity number?
    }

    // white-pink-red gradient
    this.red = 255;
    this.green = 95 + (1 - popularityRatio) * 160;
    this.blue = 95 + (1 - popularityRatio) * 160;
  }
}
