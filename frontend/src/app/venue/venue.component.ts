import { Input, Component, OnInit, OnDestroy, ViewContainerRef, ViewEncapsulation, ViewChild, TemplateRef, EventEmitter, Output } from '@angular/core';
import * as _ from 'lodash';

import { Agenda } from '../agenda/agenda';
import { Venue } from './venue';
import { VenueService } from './venue.service';
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
  selector: 'venue-form',
  templateUrl: './venue.component.html',
  styleUrls: [
    './venue.component.css'
  ]
})
export class VenueComponent implements OnInit {
  @ViewChild('templateRef') public templateRef: TemplateRef<any>;

  @Input()
  agenda: Agenda;
  @Input()
  token: string;

  @Output() onVenueAdded = new EventEmitter<Venue>();

  constructor(private venueService: VenueService,
    public modal: Modal,
    private _fb: FormBuilder) {
  }

  venueForm: FormGroup;
  formErrors: any;

  ngOnInit(): void {
  }

  createVenueModal() {
    this.formErrors = { name: "", unit: "" };
    this.venueForm = this._fb.group({
      name: [''],
      unit: ['']
    });
    
    this.modal.open(
      this.templateRef, 
      overlayConfigFactory({ isBlocking: false }, VEXModalContext)
    )
  }

  submitVenueForm(dialog: any) {
    if (this.checkVenueForm()) {
      this.createVenue(dialog);
    }
  }

  checkVenueForm():boolean{
    let isValid = true;
    if (!this.venueForm.value.name || this.venueForm.value.name.trim() === '' ) {
      this.formErrors.name = 'Required';
      isValid = false;
    }
    return isValid;
  }

  createVenue(dialog: any) {    
    this.venueService.createVenue(
      this.agenda.id, 
      this.venueForm.value.name,
      this.venueForm.value.unit
    ).subscribe(
      (data: Venue) => { 
        this.onVenueAdded.emit(data);
        dialog.close(true);
      },
      error => {
        console.log(error);
        // Map the fields returned by the server to the fields used 
        // on the client side
        const fields = {
          name: 'name', 
          unit: 'unit'
        };
        
        _.forEach(fields, (formField, serverField) => {
          if (error[serverField]) {
            this.formErrors[formField] = error[serverField].join(' ');
          }
        });
      }
    );
  }
}
