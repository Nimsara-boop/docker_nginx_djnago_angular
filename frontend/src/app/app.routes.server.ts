import {RenderMode, ServerRoute} from '@angular/ssr';

export const serverRoutes: ServerRoute[] = [
  { path: '', renderMode: RenderMode.Server },
  { path: 'login', renderMode: RenderMode.Client },
  { path: 'register', renderMode: RenderMode.Client },
  { path: 'settings', renderMode: RenderMode.Client },
  { path: 'editor/**', renderMode: RenderMode.Client },
  { path: 'article/:slug', renderMode: RenderMode.Server },
  { path: 'profile/**', renderMode: RenderMode.Server },
  { path: 'my-profile/**', renderMode: RenderMode.Client },
  { path: '**', renderMode: RenderMode.Server }
];