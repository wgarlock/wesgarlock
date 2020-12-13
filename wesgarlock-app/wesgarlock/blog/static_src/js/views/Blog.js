import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { Grid, Box, isWidthUp, withWidth, withStyles, CircularProgress } from '@material-ui/core'
import BlogCard from './BlogCard'
import Main from '../../../../base/static_src/js/views/Main'
import { request, buildUrl, pageEndpoint, parameters } from '../../../../base/static_src/js/api/request'

const styles = (theme) => ({
  blogContentWrapper: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    [theme.breakpoints.up('sm')]: {
      marginLeft: theme.spacing(4),
      marginRight: theme.spacing(4)
    },
    maxWidth: 1280,
    width: '100%'
  },
  wrapper: {
    minHeight: '60vh'
  },
  noDecoration: {
    textDecoration: 'none !important'
  },
  intersectContainer: {
    textAlign: 'center',
    marginTop: '20px',
    marginBottom: '20px'
  }

})

function getVerticalBlogPosts (width, blogPosts) {
  const gridRows = [[], [], []]
  let rows
  let xs
  if (isWidthUp('md', width)) {
    rows = 3
    xs = 4
  } else if (isWidthUp('sm', width)) {
    rows = 2
    xs = 6
  } else {
    rows = 1
    xs = 12
  }
  blogPosts.forEach((blogPost, index) => {
    gridRows[index % rows].push(
      <Grid key={blogPost.id} item xs={12}>
        <Box mb={3}>
          <BlogCard
            src={blogPost.og_image_400.url}
            title={blogPost.title}
            snippet={blogPost.intro}
            date={blogPost.date}
            url={blogPost.meta.html_url}
          />
        </Box>
      </Grid>
    )
  })
  return gridRows.map((element, index) => (
    <Grid key={index} item xs={xs}>
      {element}
    </Grid>
  ))
}

function Blog (props) {
  const { classes, width } = props
  const [blogPostState, setBlogPostState] = useState([])
  let blogPosts = []
  const limit = 6
  let offset = limit
  let objCount = 0

  function handleIntersection () {
    if (offset < objCount) {
      parameters.type = 'wesgarlockblog.BlogPage'
      parameters.limit = limit
      parameters.offset = offset
      parameters.fields = 'title,description,intro,body,tags,date,og_image_400'
      const url = buildUrl(pageEndpoint, parameters)
      request({ url, method: 'GET', body: {} }).then(data => {
        const response = JSON.parse(data)
        blogPosts = blogPosts.concat(response.items)
        setBlogPostState(blogPosts)
      }).catch(err => {
        console.log(err)
      })
      offset += limit
    }
  }

  useEffect(() => {
    if (objCount === 0) {
      parameters.type = 'wesgarlockblog.BlogPage'
      parameters.limit = limit
      parameters.fields = 'title,description,intro,body,tags,date,og_image_400'
      const url = buildUrl(pageEndpoint, parameters)
      request({ url, method: 'GET', body: {} }).then(data => {
        const response = JSON.parse(data)
        objCount = response.meta.total_count
        blogPosts = blogPosts.concat(response.items)
        setBlogPostState(blogPosts)
        const options = {
          root: null,
          rootMargin: '40px',
          threshold: 1.0
        }
        const observer = new IntersectionObserver(handleIntersection, options)
        observer.observe(document.querySelector('#intersect'))
      }).catch(err => {
        console.log(err)
      })
    }
  }, [])

  return (
    <Main>
      <Box
        display="flex"
        justifyContent="center"
        className={classNames(classes.wrapper, 'lg-p-top')}
      >
        <div className={classes.blogContentWrapper}>
          <Grid container spacing={3}>
            {getVerticalBlogPosts(width, blogPostState)}
          </Grid>
          <div id="intersect" className={classes.intersectContainer}><CircularProgress /></div>
        </div>
      </Box>
    </Main>
  )
}

Blog.propTypes = {
  classes: PropTypes.object.isRequired,
  width: PropTypes.string.isRequired,
  blogPosts: PropTypes.arrayOf(PropTypes.object)
}

export default withWidth()(withStyles(styles, { withTheme: true })(Blog))
