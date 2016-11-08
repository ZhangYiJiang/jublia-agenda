import { Input, Component, OnInit, TemplateRef, ViewChild, OnDestroy } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { Location } from '@angular/common';

import { Session } from '../session/session';
import { Agenda } from '../agenda/agenda';
import { AgendaService } from '../agenda/agenda.service';
import { DashBoardService } from '../dash-board/dash-board.service';
import { PublicAgendaService } from './public-agenda.service';
import { BoardService } from '../board/board.service';
import { GlobalVariable } from '../globals';
import { Tag } from '../tag/tag';

import { DomSanitizer, SafeResourceUrl } from "@angular/platform-browser";
import { overlayConfigFactory, Overlay, DialogRef } from 'angular2-modal';
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
import { Subscription } from 'rxjs/Subscription';

import * as _ from 'lodash';

@Component({
  selector: 'public-agenda',
  templateUrl: './public-agenda.component.html',
  styleUrls: ['./public-agenda.component.css']
})


export class PublicAgendaComponent implements OnInit, OnDestroy{
  constructor(
    private location: Location,
    private route: ActivatedRoute,
    private router: Router,
    private agendaService: AgendaService,
    private dashBoardService: DashBoardService,
    private publicAgendaService: PublicAgendaService,
    private sanitizer: DomSanitizer,
    private boardService: BoardService,
    public modal: Modal,
  ) { 
     this.subscription = boardService.openBookmarkModal$.subscribe(
      open => {
        if (open === true) {
          this.showBookmark();
        }
      }
    );
  }
  
  user = this.dashBoardService.currentUser;
  agenda: Agenda;
  email: string;
  mobile: string;
  agendaId: number;
  token : string;
  bookmarkError: string;
  mobileError: string;

  eventTags: Tag[] = [];

  bookmarkSubmitting = false;
  
  @ViewChild('infoRef') public infoRef: TemplateRef<any>;
  @ViewChild('bookmarkRef') public bookmarkRef: TemplateRef<any>;
  @ViewChild('toggleRef') public toggleRef: TemplateRef<any>;

  subscription: Subscription;

  interestedSessionIds: number[];
  interestToggleModel = false;
  defaultCategory: number;

  mapsEmbedUrl: SafeResourceUrl;

  isListView = false;
  
  ngOnInit() {
    this.route.params.forEach((params: Params) => {
      this.agendaId = params['id'];
      this.getAgendaById(this.agendaId);
      let token = params['token'];
      if (token) {
        this.getViewerByToken(token);
      }      
    });
   
  }

  getEventTags(): Tag[] { // only from first (default) category for now
    if (!this.agenda.categories[0].tags || this.agenda.categories[0].tags.length === 0) {
      return [];
    } else {
      return this.agenda.categories[0].tags;
    }
  }

  toggleView() {
    this.isListView = !this.isListView;
    console.log('list view: ' + this.isListView);
  }

  // filter tags that are not used on any sessions
  // TODO: Move this to backend
  getFilteredTags(): Tag[] {
    let tags = this.getEventTags();
    for (var i = 0; i < this.agenda.sessions.length; i++) {
      let session = this.agenda.sessions[i];
      if(session.categories == null) {
        continue;
      }
      let tagsIds = session.categories[this.defaultCategory];
      tagsIds.forEach(function(tagId: number) {
        let tag = _.find(tags, {'id': tagId});
        if(tag != null) {
          tag.used = true;
        }
      })
    }
    return _.filter(tags, {'used': true });
  }

  initTags() {
    this.defaultCategory = this.agenda.categories[0].id;
    this.eventTags = this.getFilteredTags();
    this.toggleAllTags(true);
  }

  showAll() {
    this.toggleAllTags(true);
    this.onTagFilterChange();
  }

  hideAll() {
    this.toggleAllTags(false);
    this.onTagFilterChange()
  }

  onTagFilterChange() {
    let activeTags = _.filter(this.eventTags, {toggle: true});
    for (var i = 0; i < this.agenda.sessions.length; i++) {
      let session = this.agenda.sessions[i];
      session.toggle = this.isSessionToggledByTags(session, activeTags);
    }
  }

  isSessionToggledByTags(session: Session, activeTags: Tag[]): boolean {
    if(session.categories == null) {
      // always show sessions with no tags for consistency
      return true;
    } else {
      let found = false;
      let tagsIds = session.categories[this.defaultCategory];
      tagsIds.forEach(function(tagId: number) {
        if(_.find(activeTags, {'id': tagId}) != null) {
          found = true;
        }
      })
      return found;
    }
  }

  toggleAllTags(toggle: boolean) {
    this.eventTags.forEach(function(tag) {
      tag.toggle = toggle;
    })
  }

  showInfo() {
    this.modal.open(this.infoRef, overlayConfigFactory({ isBlocking: false }, VEXModalContext));
  }

  showBookmark() {
    delete this.bookmarkError;
    this.modal.open(this.bookmarkRef, overlayConfigFactory({ isBlocking: false }, VEXModalContext));
  }

  showFilters() {
    this.modal.open(this.toggleRef, overlayConfigFactory({ isBlocking: false }, VEXModalContext));
  }

  getAgendaById(id: number) {
    this.agendaService.getAgendaById(id).subscribe(
        agenda => {
          if (!agenda.published) return;
          this.agenda = agenda;
          this.initTags();
          // Construct the iframe URL for the embedded Google Map
          if (agenda.location) {
            const url = `https://www.google.com/maps/embed/v1/place?key=${encodeURIComponent(GlobalVariable.GOOGLE_MAP_API_KEY)}&q=${encodeURIComponent(this.agenda.location)}`;
            this.mapsEmbedUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
          }
        },
        error => console.log(error)
    );
  }

  getViewerByToken(token: string) {
    this.publicAgendaService.getViewerByToken(this.agendaId, token).subscribe(
      (data: any) => {
        this.email = data.email;
        this.interestedSessionIds = data.sessions;
        this.token = token;
        this.mobile = data.mobile;
      },
      (error: any) => {
        this.location.go('/public/agenda/'+this.agendaId);
      }
    );
  }

  createToken(dialogRef: DialogRef<any>) {
    this.bookmarkSubmitting = true;
    this.publicAgendaService.createToken(this.agendaId, this.email, this.mobile).subscribe(
      (data: any) => {
        this.bookmarkSubmitting = false;
        this.router.navigate(['/public/agenda/' + this.agendaId + '/' + data.token])
        dialogRef.close();
      },
      (error: any) => {
        this.bookmarkSubmitting = false;
        console.log(error)
        if(error.email) {
          this.bookmarkError = error.email;
        }
        if(error.mobile) {
          this.mobileError = error.mobile;
        }
      }
    );
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }
}
