import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By }              from '@angular/platform-browser';
import { DebugElement }    from '@angular/core';

import { BoardComponent } from './board.component';

let comp:    BoardComponent;
let fixture: ComponentFixture<BoardComponent>;
let de:      DebugElement;
let el:      HTMLElement;

describe('BoardComponent', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ BoardComponent ], // declare the test component
    });

    fixture = TestBed.createComponent(BoardComponent);

    comp = fixture.componentInstance; // BoardComponent test instance
  });
});