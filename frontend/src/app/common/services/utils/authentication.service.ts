import { Injectable, PLATFORM_ID, inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { User } from "../../models/api/user.model";
import { BehaviorSubject, Observable } from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  private _currentUser$ = new BehaviorSubject<User | null>(null);
  private readonly _platformId = inject(PLATFORM_ID);

  public get currentUser$(): Observable<User | null> {
    return this._currentUser$.asObservable();
  }

  public get currentUserToken(): string {
    return this._isBrowser() ? localStorage.getItem('token') || '' : '';
  }

  public login(user: User) {
    if (this._isBrowser()) {
      localStorage.setItem('token', user.token);
    }
    this._currentUser$.next(user);
  }

  public logout() {
    if (this._isBrowser()) {
      localStorage.removeItem('token');
    }
    this._currentUser$.next(null);
  }

  private _isBrowser(): boolean {
    return isPlatformBrowser(this._platformId);
  }

}
