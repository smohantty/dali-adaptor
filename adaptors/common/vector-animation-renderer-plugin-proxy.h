#ifndef DALI_INTERNAL_VECTOR_ANIMATION_RENDERER_PLUGIN_PROXY_H
#define DALI_INTERNAL_VECTOR_ANIMATION_RENDERER_PLUGIN_PROXY_H

/*
 * Copyright (c) 2018 Samsung Electronics Co., Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

// INTERNAL INCLUDES
#include <vector-animation-renderer-plugin.h>

namespace Dali
{

namespace Internal
{

namespace Adaptor
{

/**
 * Proxy class to dynamically load, use and unload vector animation renderer plugin.
 */
class VectorAnimationRendererPluginProxy
{
public:

  /**
   * @brief Constructor
   */
  VectorAnimationRendererPluginProxy( const std::string& sharedObjectName );

  /**
   * @brief Destructor
   */
  ~VectorAnimationRendererPluginProxy();

  /**
   * @copydoc Dali::VectorAnimationRendererPlugin::CreateRenderer()
   */
  bool CreateRenderer( const std::string& url, Dali::Renderer renderer, uint32_t width, uint32_t height );

  /**
   * @copydoc Dali::VectorAnimationRendererPlugin::SetSize()
   */
  void SetSize( uint32_t width, uint32_t height );

  /**
   * @copydoc Dali::VectorAnimationRendererPlugin::StartRender()
   */
  bool StartRender();

  /**
   * @copydoc Dali::VectorAnimationRendererPlugin::StopRender()
   */
  void StopRender();

  /**
   * @copydoc Dali::VectorAnimationRendererPlugin::Render()
   */
  void Render( uint32_t frameNumber );

  /**
   * @copydoc Dali::VectorAnimationRendererPlugin::GetTotalFrameNumber()
   */
  uint32_t GetTotalFrameNumber();

private:

  /**
   * Dynamically loads the plugin.
   */
  void Initialize();

private:

  using CreateVectorAnimationRendererFunction = Dali::VectorAnimationRendererPlugin* (*)();

  std::string                            mSharedObjectName;   ///< Shared object name
  void*                                  mLibHandle;          ///< Handle for the loaded library
  Dali::VectorAnimationRendererPlugin*   mPlugin;             ///< Plugin handle

  CreateVectorAnimationRendererFunction  mCreateVectorAnimationRendererPtr;   ///< Function pointer called in adaptor to create a plugin instance

};

} // namespace Adaptor

} // namespace Internal

} // namespace Dali

#endif // DALI_INTERNAL_VECTOR_ANIMATION_RENDERER_PLUGIN_PROXY_H