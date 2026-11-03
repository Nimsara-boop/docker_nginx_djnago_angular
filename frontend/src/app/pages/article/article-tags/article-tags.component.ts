import { Component, EventEmitter, Output, signal, ChangeDetectionStrategy, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { TagService } from "../../../common/services/api/tag.service";
import { TagsResponse } from '../../../common/models/api/tag.model';

@Component({
  selector: 'app-article-tags',
  templateUrl: './article-tags.component.html',
  styleUrl: './article-tags.component.scss',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ArticleTagsComponent {
  @Output() tagSelected: EventEmitter<string> = new EventEmitter();

  public tags= signal<string[]>([]);
  private readonly _platformId = inject(PLATFORM_ID);

  constructor(
    private readonly _tagService: TagService
  ) {
    this._loadTags();
  }

  private _loadTags(): void {
    if (!isPlatformBrowser(this._platformId)) {
      return;
    }

    this._tagService.query().subscribe((response: TagsResponse) => {
      this.tags.set(response.tags);
    });
  }
}
