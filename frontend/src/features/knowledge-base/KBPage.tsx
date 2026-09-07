import React, { useState, useEffect } from 'react';
import { apiFetch } from '../../services/api';
import { KBArticle } from '../../types';
import { Search, BookOpen, ThumbsUp, Eye, Tag } from 'lucide-react';
import { formatDate } from '../../lib/utils';

export const KBPage: React.FC = () => {
  const [articles, setArticles] = useState<KBArticle[]>([]);
  const [search, setSearch] = useState('');
  const [selectedArticle, setSelectedArticle] = useState<KBArticle | null>(null);

  const fetchArticles = async () => {
    try {
      const queryStr = search ? `?search=${encodeURIComponent(search)}` : '';
      const data = await apiFetch<KBArticle[]>(`/knowledge-base${queryStr}`);
      setArticles(data || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchArticles();
  }, [search]);

  const handleRate = async (articleId: number, isHelpful: boolean) => {
    try {
      const updated = await apiFetch<KBArticle>(`/knowledge-base/${articleId}/feedback`, {
        method: 'POST',
        body: JSON.stringify({ is_helpful: isHelpful }),
      });
      setSelectedArticle(updated);
      fetchArticles();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-text-primary tracking-tight">Self-Service Knowledge Base</h1>
        <p className="text-xs text-text-secondary mt-0.5">
          Find solutions, setup guides, and IT troubleshooting articles
        </p>
      </div>

      {/* KB Search Bar */}
      <div className="relative">
        <Search className="w-5 h-5 absolute left-4 top-3.5 text-text-tertiary" />
        <input
          type="text"
          placeholder="Search Knowledge Base articles (e.g. VPN, Wi-Fi, Password reset)..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-12 pr-4 py-3 bg-surface border border-border rounded-2xl text-sm focus:outline-none focus:border-brand shadow-card"
        />
      </div>

      {selectedArticle ? (
        /* Selected Article Reader */
        <div className="bg-surface p-6 rounded-2xl border border-border shadow-card space-y-4">
          <button
            onClick={() => setSelectedArticle(null)}
            className="text-xs font-semibold text-brand-600 hover:underline mb-2"
          >
            ← Back to Articles
          </button>

          <h2 className="text-xl font-bold text-text-primary">{selectedArticle.title}</h2>
          <div className="flex items-center space-x-4 text-xs text-text-tertiary border-b border-border pb-3">
            <span>By {selectedArticle.author_name}</span>
            <span>•</span>
            <span className="flex items-center"><Eye className="w-3.5 h-3.5 mr-1" /> {selectedArticle.view_count} views</span>
            <span>•</span>
            <span>{formatDate(selectedArticle.created_at)}</span>
          </div>

          <div className="prose prose-sm text-text-primary max-w-none whitespace-pre-line leading-relaxed">
            {selectedArticle.content}
          </div>

          <div className="pt-4 border-t border-border flex items-center justify-between">
            <span className="text-xs text-text-secondary">Was this article helpful?</span>
            <div className="flex space-x-2">
              <button
                onClick={() => handleRate(selectedArticle.id, true)}
                className="px-3 py-1.5 rounded-xl bg-success-light text-success-dark text-xs font-semibold hover:bg-success/20 flex items-center"
              >
                <ThumbsUp className="w-3.5 h-3.5 mr-1" /> Yes ({selectedArticle.helpful_count})
              </button>
            </div>
          </div>
        </div>
      ) : (
        /* Articles List Grid */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {articles.map((article) => (
            <div
              key={article.id}
              onClick={() => setSelectedArticle(article)}
              className="bg-surface p-5 rounded-2xl border border-border shadow-card hover:shadow-card-hover cursor-pointer space-y-3 transition-all"
            >
              <div className="flex items-center space-x-2 text-brand-600">
                <BookOpen className="w-4 h-4" />
                <span className="text-xs font-bold">{article.category_name || 'General'}</span>
              </div>
              <h3 className="text-sm font-bold text-text-primary line-clamp-2">{article.title}</h3>
              <p className="text-xs text-text-secondary line-clamp-3">{article.content.replace(/[#*]/g, '')}</p>
              <div className="flex items-center justify-between text-[11px] text-text-tertiary pt-2 border-t border-border/60">
                <span>{article.view_count} views</span>
                <span className="flex items-center text-success-dark font-medium">
                  <ThumbsUp className="w-3 h-3 mr-1" /> {article.helpful_count}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
