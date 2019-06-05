import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddSentenceDialogComponent } from './add-sentence-dialog.component';

describe('AddSentenceDialogComponent', () => {
  let component: AddSentenceDialogComponent;
  let fixture: ComponentFixture<AddSentenceDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddSentenceDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddSentenceDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
