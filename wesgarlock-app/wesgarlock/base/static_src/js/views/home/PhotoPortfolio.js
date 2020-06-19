/* global context */

import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { Grid, Box, isWidthUp, withWidth, withStyles, CircularProgress } from '@material-ui/core'
import PhotoCard from '../../components/PhotoCard'
import { request, buildUrl, imageEndpoint, parameters } from '../../api/request'

const styles = (theme) => ({
  photoContentWrapper: {
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

function getPhotos (width, photos) {
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
  photos.forEach((photo, index) => {
    gridRows[index % rows].push(
        <Grid key={photo.id} item xs={12}>
          <Box mb={3}>
            <PhotoCard
              src={photo.jpeg_400}
              title={photo.title}
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

function PhotoPortfolio (props) {
  const { classes, width } = props
  const [photoState, setphotoState] = useState([])
  const limit = 6
  let offset = limit
  let objCount = 0
  let photos = []

  function handleIntersection () {
    if (offset < objCount) {
      if (context.site.public_collection) {
        parameters.collection = context.site.public_collection
      }
      parameters.limit = limit
      parameters.offset = offset
      const url = buildUrl(imageEndpoint, parameters)
      request({ url: url, method: 'GET', body: {} }).then(data => {
        const response = JSON.parse(data)
        photos = photos.concat(response.items)
        setphotoState(photos)
      }).catch(err => {
        console.log(err)
      })
      offset += limit
    }
  }

  useEffect(() => {
    if (objCount === 0) {
      if (context.site.public_collection) {
        parameters.collection = context.site.public_collection
      }
      parameters.limit = limit
      const url = buildUrl(imageEndpoint, parameters)
      request({ url: url, method: 'GET', body: {} }).then(data => {
        const response = JSON.parse(data)
        objCount = response.meta.total_count
        photos = photos.concat(response.items)
        setphotoState(photos)
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

      <Box
        display="flex"
        justifyContent="center"
        className={classNames(classes.wrapper, 'lg-p-top')}
      >
        <div className={classes.photoContentWrapper}>
          <Grid container spacing={3}>
            {getPhotos(width, photoState)}
          </Grid>
          <div id="intersect" className={classes.intersectContainer}><CircularProgress /></div>
        </div>
      </Box>

  )
}

PhotoPortfolio.propTypes = {
  classes: PropTypes.object.isRequired,
  width: PropTypes.string.isRequired
}

export default withWidth()(withStyles(styles, { withTheme: true })(PhotoPortfolio))
