import { Component, Input, EventEmitter, ElementRef } from '@angular/core';


@Component({
    selector: 'ndv-edit',
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
        
        .ndv-save {
            margin-right:3px;
        }
        
        .ndv-active {
            background-color: #f0f0f0;
            border: 1px solid #d9d9d9;
        }
        
        .ng-invalid {
            background: #ffb8b8;
            border-color: red;
        }
            
        .err-bubble {
            position: absolute;
            border: 1px solid red;
            font-size: 14px;
            background: #ffb8b8;
            padding: 6px 12px;
            width: 200px;
            line-height: 1.3;
            left: 0;
            top: 0;
            transform: translateY(calc(-100% - 10px));
        }

    `],
    template: `<span *ngIf="!permission">{{text}}</span>
               <span *ngIf="permission" class='ndv-comp' (click)='makeEditable()' [ngClass]="{'ndv-active':show}">
                   <input *ngIf='show' [ngClass]="{'ng-invalid': invalid}" (ngModelChange)="validate($event)" type='text' [(ngModel)]='text' />
                   <div class='err-bubble' *ngIf="invalid">{{error || " must contain " + min + " to -" + max +" chars."}}</div>
                   <span class='ndv-ic' *ngIf='!show'>✎ Edit</span>
                   <span *ngIf='!show'>{{text || '-Empty Field-'}}</span>
               </span>
               <div class='ndv-buttons' *ngIf='show'>
                   <a class='button primary button-symbol' (click)='callSave($event)'><i class="fa fa-check fa-fw" aria-hidden="true"></i></a>
                   <a class='button secondary button-symbol' (click)='callCancel($event)'><i class="fa fa-times fa-fw" aria-hidden="true"></i></a>
               </div>`,
    host: {
        "(document: click)": "compareEvent($event)",
        "(click)": "trackEvent($event)"
    },
    outputs: ['save : onSave']
})

export class NdvEditComponent {
    @Input('placeholder') text: any;
    @Input('title') fieldName: any;
    originalText: any;
    tracker: any;
    el: ElementRef;
    show = false;
    save = new EventEmitter;
    @Input() permission = false;
    m: Number = 3;
    @Input() min = 0;
    @Input() max = 10000;
    @Input() error: any;
    @Input() regex: any;
    invalid = false;

    constructor(el: ElementRef) {
        this.el = el;
    }
    
    ngOnInit() {
        this.originalText = this.text;    //Saves a copy of the original field info.
    }

    validate(text: any) {
        if (this.regex) {
            var re = new RegExp('' + this.regex, "ig");
            if (re.test(text)) {
                this.invalid = false;
                //console.log('valid');
            }
            else {
                this.invalid = true;
            }
        }
        else {
            if ((text.length <= this.max) && (text.length >= this.min)) {
                this.invalid = false;
            }
            else {
                this.invalid = true;
            }
        }
        //console.log(this.invalid);
    }

    makeEditable() {
        if (this.show == false) {
            this.show = true;
        }
    }

    compareEvent(globalEvent: any) {
        if (this.tracker != globalEvent && this.show) {
            this.cancelEditable();
        }
    }

    trackEvent(newHostEvent: any) {
        this.tracker = newHostEvent;
    }

    cancelEditable() {
        this.show = false;
        this.invalid = false;
        this.text = this.originalText;
    }

    callCancel(evt: any) {
        this.cancelEditable();
        evt.stopPropagation();
    }

    callSave(evt: any) {
        if (!this.invalid) {
            var data = {};  //BUILD OBJ FOR EXPORT.
            data["" + this.fieldName] = this.text;
            var oldText = this.text;
            setTimeout(() => { this.originalText = oldText; this.text = oldText }, 0);  //Sets the field with the new text;
            this.save.emit(data);
            this.show = false;
        }
        evt.stopPropagation();
    }
}