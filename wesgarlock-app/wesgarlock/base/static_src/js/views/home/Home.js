/* global context */

import React, { Fragment } from 'react'
import HeadSection from './HeadSection'
import Main from '../Main'
import PhotoPortfolio from './PhotoPortfolio'

function Home (props) {
  return (
    <Main>
      <Fragment>
        <HeadSection
          title={context.site.site.site_name}
          text={context.page.description}
          button={context.page.primary_page}
          image={context.page.hero_image}/>
      </Fragment>
      <PhotoPortfolio />
    </Main>
  )
}

export default Home
