import {Component, Input, EventEmitter, ElementRef, HostListener} from '@angular/core';
import * as moment from "moment";


@Component({
    selector: 'ndv-date',
    styles: [`
        :host {
            position: relative;
        }
        
        .ndv-ic {
            position: absolute;
            top: 0;
            left: -1px;
            transform: translateY(-100%);
            padding: 3px 6px 3px 4px;
            
            background: #888;
            color: #fff;
            font-size: 13px;
            line-height: 1;
            font-weight: normal;
            white-space: nowrap;
            
            display: none;
        }
        
        .ndv-comp:hover .ndv-ic {
            display: block;
        }

        .ndv-comp {
            padding: 6px;
            border-radius: 3px;
            border: 1px solid #ccc;
            min-width: 50px;
            display: inline-block;
            position: relative;
        }
        
        .ndv-comp:hover {
            border-radius: 0 3px 3px 3px;
        }
        
        .active-ndv {
            background-color: #f0f0f0;
            border: 1px solid #d9d9d9;
        }
        
        form {
            display: inline;
        }
        
        input {
            border-radius: 5px;
            box-shadow: none;
            border: 1px solid #dedede;
            min-width: 5px;
        }
        
        .ndv-buttons {
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            border-top: none;
            border-radius: 0 0 3px 3px;
            box-shadow: 0 3px 6px rgba(111,111,111,0.2);
            outline: none;
            padding: 3px;
            position: absolute;
            width: 80px;
            left: 6px;
            top: 100%;
            z-index: 1;
            font-size: 1.1rem;
            line-height: 1.5rem;
        }
        
        .ndv-comp:hover {
            border-color: #999;
        }
    `],
    template: `<span *ngIf="!permission">{{date}}</span>
               <span *ngIf="permission" class='ndv-comp' (click)='makeEditable()' [ngClass]="{'ndv-active':show}">
                   <form (submit)="callSave($event)">
                       <input *ngIf='show' type='date' [(ngModel)]='date' [ngModelOptions]="{standalone: true}" />
                       <span class='ndv-ic' *ngIf='!show'>✎ Edit</span>
                       <span *ngIf='!show'>{{date || 'Empty'}}</span>
                   
                       <span class='ndv-buttons' *ngIf='show'>
                           <a class='button primary button-symbol' (click)='callSave($event)'><i class="fa fa-check fa-fw" aria-hidden="true"></i></a>
                           <a class='button secondary button-symbol' (click)='callCancel($event)'><i class="fa fa-times fa-fw" aria-hidden="true"></i></a>
                       </span>
                   </form>
               </span>`,
    host: {
        "(document: click)": "compareEvent($event)",
    },
    outputs: ['save : onSave']
})

export class NdvEditDateComponent {
    @Input('placeholder') holder: any;
    @Input('title') fieldName: any;
    @Input() permission = true;
    date: any;
    originalDate: any;
    editedDate: any;
    tracker: any;
    el: ElementRef;
    show = false;
    save = new EventEmitter;

    constructor(el: ElementRef) {
        this.el = el;
    }
    
    ngOnInit() {
        this.date = moment(this.holder).format('YYYY-MM-DD');
        this.originalDate = this.date;    //Saves a copy of the original field info.
    }

    makeEditable() {
        if (this.show == false) {
            // Restore the user's last saved text, if possible
            if (this.editedDate) {
                this.date = this.editedDate;
            }

            this.show = true;
        }
    }

    compareEvent(globalEvent: any) {
        if (this.tracker != globalEvent && this.show) {
            this.cancelEditable();
        }
    }

    @HostListener('click', ['$event']) trackEvent(newHostEvent: any) {
        this.tracker = newHostEvent;
    }

    cancelEditable(resetInput: boolean = false) {
        // Save a copy of the text the user was editing
        if (!resetInput) {
            this.editedDate = this.date;
        } else {
            this.editedDate = null;
        }

        this.show = false;
        this.date = this.originalDate;
    }

    callCancel(evt: any) {
        this.cancelEditable(true);
        evt.stopPropagation();
    }

    callSave(evt: any) {
        const date = this.date;
        const data = {};  //BUILD OBJ FOR EXPORT.
        data["" + this.fieldName] = date;

        setTimeout(() => {
            this.editedDate = null;
            this.originalDate = date;
            this.date = date;
        }, 0);  //Sets the field with the new text;

        this.save.emit(data);
        this.show = false;

        evt.stopPropagation();
        evt.preventDefault();
    }
}