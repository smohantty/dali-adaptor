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

// CLASS HEADER
#include <dali/internal/system/windows/callback-manager-win.h>

// EXTERNAL INCLUDES
//#include <uv.h>
#include <dali/integration-api/debug.h>
#include <Win32WindowSystem.h>

// INTERNAL INCLUDES
#include <Windows.h>

namespace Dali
{

namespace Internal
{

namespace Adaptor
{

WinCallbackManager::WinCallbackManager()
:mRunning(false)
{
}

void WinCallbackManager::Start()
{
  DALI_ASSERT_DEBUG( mRunning == false );
  mRunning = true;
}

void WinCallbackManager::Stop()
{
  // make sure we're not called twice
  DALI_ASSERT_DEBUG( mRunning == true );

  mRunning = false;
}

#define WIN_CALLBACK_EVENT    9999

bool WinCallbackManager::AddIdleCallback( CallbackBase* callback )
{
  if( !mRunning )
  {
    return false;
  }

  Win32WindowSystem::AddListener( WIN_CALLBACK_EVENT, callback );
  Win32WindowSystem::PostWinMessage( WIN_CALLBACK_EVENT, (long)callback, 0 );
  return true;
}

void WinCallbackManager::RemoveIdleCallback( CallbackBase* callback )
{
  //Wait for deal
}

// Creates a concrete interface for CallbackManager
CallbackManager* CallbackManager::New()
{
  return new WinCallbackManager;
}

} // namespace Adaptor

} // namespace Internal

} // namespace Dali