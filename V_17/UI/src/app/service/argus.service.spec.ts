import { TestBed } from '@angular/core/testing';

import { ArgusService } from './argus.service';

describe('ArgusService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ArgusService = TestBed.get(ArgusService);
    expect(service).toBeTruthy();
  });
});
