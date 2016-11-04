import { Input, Component, OnInit, OnDestroy, ViewContainerRef, ViewEncapsulation, ViewChild, TemplateRef, EventEmitter, Output } from '@angular/core';
import * as _ from 'lodash';

import { Agenda } from '../agenda/agenda';
import { Speaker } from './speaker';
import { SpeakerService } from './speaker.service';
import { GlobalVariable } from '../globals';

import { DOMUtilService } from '../util/dom.util.service';
import { overlayConfigFactory } from 'angular2-modal';
import { Overlay } from 'angular2-modal';
import { FormGroup, FormControl, FormBuilder, FormArray, Validators } from '@angular/forms';
import { Observable } from 'rxjs/Rx';
import * as $ from 'jquery';

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
  selector: 'speaker-form',
  templateUrl: './speaker.component.html',
  styleUrls: [
    './speaker.component.css'
  ]
})
export class SpeakerComponent implements OnInit {
  @ViewChild('templateRef') public templateRef: TemplateRef<any>;

  @Input()
  agenda: Agenda;
  @Input()
  token: string;

  @Output() onSpeakerAdded = new EventEmitter<Speaker>();

  constructor(private speakerService: SpeakerService,
    public modal: Modal,
    private _fb: FormBuilder) {
  }

  speakerForm: FormGroup;
  formErrors: any;

  ngOnInit(): void {
  }

  createSpeakerModal() {
    this.formErrors = { name: "", company: "", position: "", profile: "", email: "", phone_number: "", company_description: "", company_url: "" };
    this.speakerForm = this._fb.group({
        name: [''],
        company: [''],
        position: '',
        profile: '',
        email: '',
        phone_number: '',
        company_description: '',
        company_url: '',
    });
    
    this.modal.open(
      this.templateRef, 
      overlayConfigFactory({ isBlocking: false }, VEXModalContext)
    )
  }

  submitSpeakerForm(dialog: any) {
    if (this.checkSpeakerForm()) {
      this.createSpeaker(dialog);
    }
  }

  checkSpeakerForm():boolean{
    let isValid = true;
    if (!this.speakerForm.value.name || this.speakerForm.value.name.trim() === '' ) {
      this.formErrors.name = 'Required';
      isValid = false;
    }
    if (!this.speakerForm.value.company || this.speakerForm.value.company.trim() === '' ) {
      this.formErrors.company = 'Required';
      isValid = false;
    }
    return isValid;
  }

  createSpeaker(dialog: any) {
    let company_url = this.speakerForm.value.company_url;
    if (company_url && !company_url.match(/^https?:\/\//i)) {
      company_url = 'http://' + company_url;
    }
    this.speakerService.createSpeaker(
      this.agenda.id, 
      this.speakerForm.value.name, 
      this.speakerForm.value.company, 
      this.speakerForm.value.profile,
      this.speakerForm.value.position, 
      this.speakerForm.value.email, 
      this.speakerForm.value.phone_number, 
      this.speakerForm.value.company_description, 
      company_url
    ).subscribe(
      (data: Speaker) => { 
        this.onSpeakerAdded.emit(data);
        dialog.close(true);
      },
      errors => {
        this.formErrors = errors;
      }
    );
  }
}
