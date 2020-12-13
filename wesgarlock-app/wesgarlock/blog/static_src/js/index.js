/* global context */

import React from 'react'
import ReactDOM from 'react-dom'

import BlogPageIndex from './views/blog_index_page'
import BlogPage from './views/blog_page'

export function App () {
  let page

  if (context.page.content_type === 32 && context.page.live) {
    page = <BlogPageIndex />
  } else if (context.page.content_type === 31) {
    page = <BlogPage />
  }
  return (page)
}

ReactDOM.render(<App />, document.getElementById('react-container'))
