import {Component, Input, EventEmitter, ElementRef, HostListener} from '@angular/core';


@Component({
    selector: 'ndv-area',
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
            min-width: 60px;
            display: block;
            position: relative;
        }
        
        .ndv-comp:hover {
            border-radius: 0 3px 3px 3px;
        }
        
        .active-ndv {
            background-color: #f0f0f0;
            border: 1px solid #d9d9d9;
        }
        
        textarea {
            border-radius: 5px;
            box-shadow: none;
            border: 1px solid #dedede;
            width: 100%;
            line-height: inherit;
            resize: vertical;
        }
        
        .ndv-buttons {
            border: 1px solid #ccc;
            border-top: none;
            border-radius: 0 0 3px 3px;
            box-shadow: 0 3px 6px rgba(111,111,111,0.2);
            outline: none;
            padding: 5px;
            position: absolute;
            top: 100%;
            left: 6px;
            z-index: 1;
            font-size: 1.1rem;
            line-height: 1.5rem;
            background-color: #f0f0f0;
        }
        
        .ndv-comp:hover {
            border: 1px solid grey;
        }
    `],
    template: `<div *ngIf="!permission">{{text}}</div>
               <form *ngIf="permission" class='ndv-comp' (click)='makeEditable()' (submit)="callSave($event)" [ngClass]="{'ndv-active':show}">
                   <div>
                       <textarea rows="6" cols="55" *ngIf='show' [(ngModel)]='text' [ngModelOptions]='{standalone: true}'></textarea>
                       <span class='ndv-ic' *ngIf='!show'>✎ Edit</span>
                       <span *ngIf='!show'>{{text || 'Empty'}}</span>
                   </div>
                   <div class='ndv-buttons' *ngIf='show'>
                       <a class='button primary button-symbol' (click)='callSave($event)'><i class="fa fa-check fa-fw" aria-hidden="true"></i></a>
                       <a class='button secondary button-symbol' (click)='callCancel($event)'><i class="fa fa-times fa-fw" aria-hidden="true"></i></a>
                   </div>
               </form>`,
    host: {
        "(document: click)": "compareEvent($event)",
    },
    outputs: ['save : onSave']
})

export class NdvEditAreaComponent {
    @Input('placeholder') text: any;
    @Input('title') fieldName: any;
    @Input() permission = true;
    editedText: any;
    originalText: any;
    tracker: any;
    el: ElementRef;
    show = false;
    save = new EventEmitter;

    constructor(el: ElementRef) {
        this.el = el;
    }
    
    ngOnInit() {
        this.originalText = this.text;    //Saves a copy of the original field info.
    }

    makeEditable() {
        if (this.show == false) {
            // Restore the user's last saved text, if possible
            if (this.editedText) {
                this.text = this.editedText;
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
            this.editedText = this.text;
        } else {
            this.editedText = null;
        }

        this.show = false;
        this.text = this.originalText;
    }
    
    callCancel(evt: any) {
        this.cancelEditable(true);
        evt.stopPropagation();
    }

    callSave(evt: any) {
        const text = this.text;
        const data = {};  //BUILD OBJ FOR EXPORT.
        data["" + this.fieldName] = text;

        setTimeout(() => {
            this.editedText = null;
            this.originalText = text;
            this.text = text;
        }, 0);  //Sets the field with the new text;

        this.save.emit(data);
        this.show = false;
        
        evt.stopPropagation();
        evt.preventDefault();
    }
}